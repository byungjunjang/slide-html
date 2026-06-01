param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$ProjectName,

  [Parameter(Mandatory = $false, Position = 1)]
  [string]$DesignSystem
)

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$SkillDir = (Resolve-Path -LiteralPath (Join-Path $ScriptDir "..")).Path
$TemplatesDir = Join-Path $SkillDir "templates"
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $SkillDir "..\..\..")).Path
$ProjectDir = Join-Path $RepoRoot "output\$ProjectName-pptx"
$DsRoot = Join-Path $SkillDir "assets\design-systems"
$ActiveJson = Join-Path $DsRoot "active.json"

if ([string]::IsNullOrWhiteSpace($DesignSystem)) {
  if (Test-Path -LiteralPath $ActiveJson) {
    $DesignSystem = (Get-Content -Raw -Encoding UTF8 -LiteralPath $ActiveJson | ConvertFrom-Json).active
    $DsReason = "active.json"
  } else {
    $DesignSystem = "jangpm"
    $DsReason = "fallback default"
  }
} else {
  $DsReason = "explicit"
}

Write-Output "[design-system] $DesignSystem ($DsReason)"

$DsSource = Join-Path $DsRoot $DesignSystem
if (-not (Test-Path -LiteralPath $DsSource -PathType Container)) {
  Write-Error "Design system preset not found: $DesignSystem"
}
if (Test-Path -LiteralPath $ProjectDir) {
  Write-Error "Project already exists: $ProjectDir"
}

New-Item -ItemType Directory -Force -Path `
  (Join-Path $ProjectDir "slides"), `
  (Join-Path $ProjectDir "icons"), `
  (Join-Path $ProjectDir "images"), `
  (Join-Path $ProjectDir "diagrams") | Out-Null

Copy-Item -LiteralPath $DsSource -Destination (Join-Path $ProjectDir "design-system") -Recurse

$PresetCss = Join-Path $DsSource "_pptx-slide.css"
if (-not (Test-Path -LiteralPath $PresetCss -PathType Leaf)) {
  Write-Error "Preset $DesignSystem is missing _pptx-slide.css. Generate it via /theme-init."
}
Copy-Item -LiteralPath $PresetCss -Destination (Join-Path $ProjectDir "_pptx-slide.css")

Copy-Item -LiteralPath (Join-Path $TemplatesDir "build.mjs.template") -Destination (Join-Path $ProjectDir "build.mjs")

$TitleSlide = Join-Path $DsSource "pptx-boilerplate\01-title.html"
if (-not (Test-Path -LiteralPath $TitleSlide -PathType Leaf)) {
  Write-Error "Preset $DesignSystem is missing pptx-boilerplate/01-title.html. Generate it via /theme-init."
}
Copy-Item -LiteralPath $TitleSlide -Destination (Join-Path $ProjectDir "slides\01-title.html")

$Readme = @(
  "# $ProjectName (editable PPTX)"
  ""
  "Generated: $(Get-Date -Format yyyy-MM-dd) · design system: $DesignSystem"
  ""
  "## Workflow"
  ""
  "1. Author slide HTML files under ``slides/`` using ``NN-name.html`` filenames."
  "2. Keep every slide within ``/slide`` 4 hard constraints."
  "3. Build from this folder:"
  ""
  "   ``````bash"
  "   node build.mjs"
  "   ``````"
  ""
  "4. Result: ``$ProjectName.pptx`` in this project folder."
  ""
  "## Root dependencies"
  ""
  "``````bash"
  "cd $RepoRoot"
  "npm install"
  "npx playwright install chromium"
  "``````"
) -join [Environment]::NewLine
Set-Content -LiteralPath (Join-Path $ProjectDir "README.md") -Encoding UTF8 -Value $Readme

Write-Output ""
Write-Output "✓ Project created: $ProjectDir"
Write-Output ""
Write-Output "  ├── slides/01-title.html"
Write-Output "  ├── icons/"
Write-Output "  ├── images/"
Write-Output "  ├── diagrams/"
Write-Output "  ├── design-system/ ($DesignSystem copy)"
Write-Output "  ├── _pptx-slide.css"
Write-Output "  ├── build.mjs"
Write-Output "  └── README.md"
Write-Output ""
Write-Output "Build result: $ProjectDir\$ProjectName.pptx"

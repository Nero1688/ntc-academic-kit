# 東專學術 AI 工具包 安裝腳本（Windows PowerShell 5.1 以上）
# 用途：把 skills 資料夾下的十支技能複製到
#   <TargetRoot>\.claude\skills   （Claude Code 個人技能目錄）
#   <TargetRoot>\.agents\skills   （Codex 個人技能目錄）
# 若目標已有同名資料夾，會先改名為「名稱.bak-yyyyMMdd」再複製。
# 不需要系統管理員權限、不修改系統設定、不下載任何東西。
#
# 用法：
#   .\install_windows.ps1                      安裝到你的使用者家目錄
#   .\install_windows.ps1 -DryRun              只顯示會做什麼，不實際複製
#   .\install_windows.ps1 -TargetRoot D:\測試   安裝到指定目錄
param(
    [string]$TargetRoot = $HOME,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$kitRoot   = Split-Path -Parent $PSScriptRoot
$skillsSrc = Join-Path $kitRoot 'skills'
$skillNames = @('kit-guide','topic-scout','lit-search','lit-matrix','writing-coach',
                'paper-selfcheck','grant-writer','ai-disclosure','prompt-coach','opendata-scout')
$targets = @(
    @{ Label = 'Claude Code'; Path = (Join-Path $TargetRoot '.claude\skills') },
    @{ Label = 'Codex';       Path = (Join-Path $TargetRoot '.agents\skills') }
)
$stamp = Get-Date -Format 'yyyyMMdd'

if (-not (Test-Path -LiteralPath $skillsSrc)) {
    Write-Host "找不到技能來源資料夾：$skillsSrc" -ForegroundColor Red
    exit 1
}
foreach ($n in $skillNames) {
    if (-not (Test-Path -LiteralPath (Join-Path $skillsSrc $n))) {
        Write-Host "來源缺少技能資料夾：$n" -ForegroundColor Red
        exit 1
    }
}

if ($DryRun) { Write-Host '【試跑模式 DryRun】只顯示動作，不會複製或改名任何檔案。' -ForegroundColor Yellow }
Write-Host "安裝根目錄：$TargetRoot"
Write-Host ''

$installed = 0
$backedUp  = 0
foreach ($t in $targets) {
    Write-Host ("[{0}] 目標：{1}" -f $t.Label, $t.Path) -ForegroundColor Cyan
    if (-not (Test-Path -LiteralPath $t.Path)) {
        if ($DryRun) { Write-Host '  將建立目標目錄' }
        else { New-Item -ItemType Directory -Path $t.Path -Force | Out-Null }
    }
    foreach ($n in $skillNames) {
        $src = Join-Path $skillsSrc $n
        $dst = Join-Path $t.Path $n
        if (Test-Path -LiteralPath $dst) {
            $bak = "$dst.bak-$stamp"
            $i = 2
            while (Test-Path -LiteralPath $bak) { $bak = "$dst.bak-$stamp-$i"; $i++ }
            if ($DryRun) { Write-Host ("  將舊版改名：{0} -> {1}" -f $n, (Split-Path -Leaf $bak)) }
            else {
                Rename-Item -LiteralPath $dst -NewName (Split-Path -Leaf $bak)
                Write-Host ("  已備份舊版：{0} -> {1}" -f $n, (Split-Path -Leaf $bak))
            }
            $backedUp++
        }
        if ($DryRun) { Write-Host ("  將複製：{0}" -f $n) }
        else {
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
            Write-Host ("  已安裝：{0}" -f $n)
        }
        $installed++
    }
}

Write-Host ''
if ($DryRun) {
    Write-Host ("試跑完成：預計安裝 {0} 項、備份 {1} 項。確認無誤後，不加 -DryRun 再執行一次。" -f $installed, $backedUp) -ForegroundColor Yellow
} else {
    Write-Host ("安裝完成：共 {0} 項，備份舊版 {1} 項。" -f $installed, $backedUp) -ForegroundColor Green
    Write-Host '下一步：關閉並重新開啟 Claude Code 或 Codex，輸入「請用 kit-guide 帶我開始」確認技能可用。'
}

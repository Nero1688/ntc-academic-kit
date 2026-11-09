# 東專學術 AI 工具包（ntc-academic-kit）

給專題學生與一般教師的學術 AI 技能包。十支技能放在 `skills/`，**同一份資料夾**可以給 Claude Code 與 Codex 使用。每支技能都內建學術倫理防線：不編造、不代寫、不外流、留紀錄。

版本：v1.1（2026-11）

## 十支技能一覽

| 技能 | 做什麼 | 什麼時候用 |
|---|---|---|
| kit-guide | 問兩三個問題，指到最適合的技能 | 不知道從哪裡開始 |
| topic-scout | 找專題題目、初選方法、第一週行動清單 | 沒題目或題目太大 |
| lit-search | 關鍵詞、資料庫建議、逐筆查文獻真偽與撤稿 | 找文獻、確認 AI 給的文獻是真的 |
| lit-matrix | 文獻比較表、研究缺口、英文論文精讀 | 讀了一堆文獻很亂 |
| writing-coach | 學生模式（教練，不代寫）與研究者模式（潤飾） | 寫大綱、改段落、去 AI 腔 |
| paper-selfcheck | 數字、引用、APA、簡易模擬審查的核取表 | 繳交前、投稿前 |
| grant-writer | 計畫書結構整理與審查人視角自評 | 國科會、教學實踐、大專學生研究計畫 |
| ai-disclosure | AI 使用紀錄、揭露聲明、紅線檢查、去識別化清單 | 繳交前、不確定能不能用 AI |
| prompt-coach | 把模糊提示改成精準提示 | 覺得 AI 回答不準 |
| opendata-scout | 把研究問題轉成資料需求，到政府公開資料目錄找次級資料，檢查授權並寫下資料來源紀錄 | 專題要用統計資料、不知道資料去哪找 |

## 三步驟安裝

1. 到 https://github.com/Nero1688/ntc-academic-kit ，按綠色的「Code」按鈕選「Download ZIP」，下載後解壓縮整個資料夾。會用 Git 的話，也可以執行 `git clone https://github.com/Nero1688/ntc-academic-kit.git`。
2. 在 Windows 上，對 `install\install_windows.ps1` 按右鍵選「用 PowerShell 執行」；或開啟 PowerShell，先試跑：
   `powershell -ExecutionPolicy Bypass -File .\install\install_windows.ps1 -DryRun`
   確認無誤後，去掉 `-DryRun` 再執行一次。macOS 或不想用腳本，請看 `install\手動安裝說明.md`。
3. 關閉並重新開啟 Claude Code 或 Codex，輸入：「請用 kit-guide 帶我開始」。

腳本不需要系統管理員權限、不改系統設定、不下載任何東西；已有同名技能時，舊版會先改名為「名稱.bak-日期」。

## 專題資料夾範本

`project-template/` 內有 CLAUDE.md 與 AGENTS.md（內容相同）、AI使用紀錄.md、01_文獻 到 04_資料 資料夾與 .gitignore。開新專題時整個複製過去，AI 助理會讀到研究守則。

## 做自己的 skill（skill-template）

`skill-template/` 在工具包根目錄，**不是**技能，安裝腳本不會複製它。裡面有 SKILL.md 範本（六個固定段落，倫理防線已預填）與〈做自己的skill.md〉白話教學：寫下作業流程、請 AI 助理依範本產生、用真實案例試跑、修一次。課堂上可以用它做出專屬你自己研究的技能。

## 第一次使用的三句提示

1. 「請用 kit-guide 帶我開始，我是餐旅管理科的學生，還沒有題目。」
2. 「請用 topic-scout 幫我找專題題目。」
3. 「請用 prompt-coach 檢查我這個問題問得好不好：[貼上你的問題]」

## 倫理聲明

- **你負責**：作品是你的，AI 只是工具，內容對錯由你承擔。
- **你查證**：AI 給的文獻、數字、規定，都要對照原文；查不到就是查不到。
- **你揭露**：用了 AI 就依老師、學校或期刊的規定揭露，並記到 AI使用紀錄.md。
- 學生作業採教練模式，不代寫整篇；不要把含個資的資料或他人未公開的稿件貼給 AI。
- 技能內容中的規範與計畫格式都是查證當時的摘要，會更新，**以官方原文與當年度公告為準**。

## 授權與作者

- 作者：林義棠
- 授權：本工具包採用創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際授權條款（CC BY-NC-SA 4.0）。你可以自由使用、修改與分享，但要標示作者、不得用於商業目的，改作也要用相同授權分享。條款全文見 `LICENSE` 與 https://creativecommons.org/licenses/by-nc-sa/4.0/ 。

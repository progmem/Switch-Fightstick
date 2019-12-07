# 未完成です

## Switch-Fightstick
マイコンをコントローラに偽装してSwitchと通信を行えるようにするプロジェクト  
Fork元なのでそちらや解説してくれてるサイトを要参照

## About this project
AVRマイコンとPC(+キャプボ)を用いてポケモン剣盾における以下の操作の自動化が目的です  
- 非バグ技
  - バトルタワー周回
  - トーナメント周回
  - 卵孵化/厳選/色粘り
  - A連打 > 穴掘り兄弟とか
- バグ技(日付変更バグ いつか修正されるかも)
  - ワット回収
  - レイド厳選
  - idくじ
  - などなど...時渡り全般
  
本プロジェクトではキャプボを使わない動作/軽い動作はマイコン独立で,  
それ以外はPCに繋いで動作させるつもりです  
操作切り替えはPCからすべて行う予定(組み込みの知識が乏しいので)  
  
#### 現在実行可能な操作  
なし

## What you need
- ハードウェア
  - ATMega16U2 / ATMega32U4 Board
  - USBシリアル変換アダプタ
  - 
- ソフトウェア
  
プログラム完成次第順次リンクを添えて追加していくつもりです  

## How it works
完成次第載せます
  
## References
PCからSwitchへの通信のやり方 おいら屋ファクトリー  
https://blog.feelmy.net/control-nintendo-switch-from-computer/  
  
ATmega16U2へdfu-programmerでカスタムファームを書き込み  
https://another.maple4ever.net/archives/2380/  
  
Arduino-Switch間の無限ワットプログラム配布  
某掲示板の無限ワットスレ リンク略 調べたら多分出ます  
  
PC-ATmegaマイコン-PCを繋いでる プログラムを参考にさせていただきました  
https://github.com/ebith/Switch-Fightstick  
  
その他沢山のブログ等を参考にさせていただいています

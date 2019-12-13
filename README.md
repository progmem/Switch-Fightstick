## Fork元: Switch-Fightstick
マイコンをコントローラに偽装してSwitchと通信を行えるようにするプロジェクト  
有名なプロジェクトなので詳しくはそちらのReadmeや解説してくれてるサイトを参照してください  

## Abstract
ポケモン剣盾の自動化ソフトウェア  
マイコンやPythonで書いた自動化コードをPCで切り替えて操作できます  
またマイコンに書き込んだコードはPCとの接続を切っても動き続けます  

リリース前参考画像
![リリース前GUI](https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/pokecon_gui_before_release.PNG)

## Releases
未定ですが年内に画像認識を用いた自動化を書いた時点で1つリリースとして区切る予定です  
その後も下記目標までリリースを続けていきます  

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
  
自動化以外の目的としては
+ マクロ作成機能(Pythonコード/マイコン書き込み)  
+ 取得情報の記録と通知  
+ 不測挙動時の自動停止 など  
  
本プロジェクトではキャプボを使わない動作/軽い動作はマイコン独立で,  
それ以外はPCに繋いで動作させるつもりです  
既存マクロの切り替えやPCで作成したマクロのマイコン/.cファイルへの書き込みはPCからすべて行う予定  
  
### 現在実行可能な操作  
現バージョンではデバグの効率化のためコントローラの接続画面から開始する必要があります  
  
- ワット自動化
0. 無限ワット対象の巣の200W/2000Wの光は消しておく.   
   レイドのある巣を選ぶ場合倒しておくかレイドの無い巣を選ぶ  
   またSwitch側の本体設定で「インターネットで時間を合わせる」をONにしておく  
1. 「ねがいのかたまり」を巣に投げてレポート書いた後, 話しかけずに待機  
2. .hex書き込み済みのマイコンを接続   
  
- A連打
  
- IDくじ&ワット自動化
  
主要部分が完成したらきちんと載せるつもりです  
現在これらコマンドはすべてReferenceの配布スレから拝借  
  
## What you need
- ハードウェア
  - ATMega16U2 / ATMega32U4 Board
  - USBシリアル変換アダプタ
  - ジャンパワイヤー
  - キャプチャボード
- ソフトウェア
  - WinAVR
  - dfu-programmer
  
足りない分は順次載せていきます  
自分のハードウェア環境は次のようになってます  
- ELEGOO Arduino Uno R3  
リンクは完コピ製品らしいので気にする方はオリジナルを購入してください  
https://www.amazon.co.jp/gp/product/B06Y5TBNQX

- FTDI USBシリアル変換アダプター Rev.2  
https://www.amazon.co.jp/gp/product/B01LVXGT04

- WayinTop ブレボ/ジャンパワイヤーキット  
dfuモードに入るのに1本, マイコンとUSBシリアル変換に4本使います  
なのでこんなに必要ないですが, ついでにArduino触りたかったのでこれ買ってます  
https://www.amazon.co.jp/gp/product/B07WYYLS82

- I-O DATA USB-HDMI UVCキャプチャボード GV-HUCV
https://www.amazon.co.jp/gp/product/B07CZRHX2V

## How it works
PC-Arduino-Switchでの通信ができたので初回リリースを出したタイミングで詳しい説明を更新予定です  
マイコン-Switchでの自動化はReferencesに乗せてる配布スレを参照のこと  

繋ぎ方は次のようになります（画像横向いちゃってるので後で直しときます）  
左: Arduino Uno R3  右: USBシリアル変換アダプタ  
白ワイヤ: dfuモード用  
それ以外: Arduino-変換アダプタ接続用  
  
![シリアル変換接続](https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/arduino_serial_connection.JPG)  
  
接続状態  
Switch-(USB_A-USB_B)-Arduino Uno R3-(ワイヤ接続)-シリアル変換アダプタ-(USB_micro_B-USB_A)-PC  
  
## References
Arduino-Switch間の無限ワットプログラム配布をしてくれた所  
マイコン-Switchでの実行はここで教わりました アクセスできなくなったら詳細も載せます  
https://medaka.5ch.net/test/read.cgi/poke/1574816324/

キャプボを用いたPC-AVRマイコン-Switch操作の先行者です  
NYSLライセンスということで本当に色々使わせてもらってます  
[Switch版DEAD OR ALIVE Xtreme3 Scarlet (DOAX3S) 自動プレイ](https://randdtips.com/switch-doax3s-autoplay/)
  
[PCからSwitchへの通信のやり方 おいら屋ファクトリー](https://blog.feelmy.net/control-nintendo-switch-from-computer/)

[ATmega16U2へdfu-programmerでカスタムファームを書き込み](https://another.maple4ever.net/archives/2380/)
  
PC-ATmegaマイコン-PCを繋いでる プログラムを参考にさせていただきました  
https://github.com/ebith/Switch-Fightstick  
  
その他沢山のブログ等を参考にさせていただいています  
また本プロジェクトでは自動化コード(それ以外でも)のプルリクエスト歓迎してます!  

## Abstract
ポケモン剣盾の自動化ソフトウェア  
マイコンやPythonで書いた自動化コードを抜き差しなくPCで切り替えて操作できます  
またマイコンに書き込んだコードはPCとの接続を切っても動き続けます  

リリース前参考画像
![リリース前GUI](https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/pokecon_gui_before_release.PNG)

## Releases
[リリースについて](https://github.com/KawaSwitch/Poke-Controller/wiki/About-Releases)  
以降も下記目標までリリースを続けていきます  

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
+ PythonコードからのMCU変換  
+ 取得情報の記録と通知  
+ 不測挙動時の自動停止 など  
  
本プロジェクトではキャプボを使わない動作/軽い動作はマイコン独立で,  
それ以外はPCに繋いで動作させるつもりです  
既存マクロの切り替えやPCで作成したマクロのマイコン/.cファイルへの書き込みはPCからすべて行う予定  

## How to use  
こちらで解説しています  
[Poke-Controllerの使い方](https://github.com/KawaSwitch/Poke-Controller/wiki/Poke-Controller%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9)  

分からないことがあれば遠慮なく[Issue](https://github.com/KawaSwitch/Poke-Controller/issues)まで  
[Q&A](https://github.com/KawaSwitch/Poke-Controller/wiki/Q&A)や[解決済みIssue](https://github.com/KawaSwitch/Poke-Controller/issues?q=is%3Aissue+is%3Aclosed)なども役に立つかもしれません  
  
### 現在のデフォルトのコマンド 
  
- MCU  
  - A連打  
    その名の通りです  
  
  - リーグ自動周回  
    [発案元](http://niwaka-syndrome.blog.jp/archives/20509394.html) を要参照  
    準備完了後, 受付に話しかけられる状態からスタートしてください  

  - ワット自動化  
    無限ワット対象の巣の200W/2000Wの光は消しておく.   
    レイドのある巣を選ぶ場合倒しておくかレイドの無い巣を選ぶ.  
    またSwitch側の本体設定で「インターネットで時間を合わせる」を**ON**にしておく.  
    
    1: 「ねがいのかたまり」を巣に投げてレポート書いた後, 話しかけずに待機  
    2: .hex書き込み済みのマイコンを接続   
    
    [提供元](https://medaka.5ch.net/test/read.cgi/poke/1574816324/)の>>25を参照  
  
- Python  
  下記の記事を参考にしてください  
  [シリアル通信のデフォルト実装コマンド](https://github.com/KawaSwitch/Poke-Controller/wiki/%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E3%81%AE%E5%AE%9F%E8%A3%85%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89(%E3%82%B7%E3%83%AA%E3%82%A2%E3%83%AB%E9%80%9A%E4%BF%A1-Python))

  <br>

既存のコマンドは順次移植/追加予定で自作も上げていきます  
[プルリクエスト](https://github.com/KawaSwitch/Poke-Controller/pulls)も受け付けています

### コマンドの書き方
必要なコマンドは自分で簡単に書いて追加することができます  
MCUとPythonの双方を選択可能ですがPythonを強く推奨します  
+ 実時間形式で秒を単位として書くことができます
+ ループや条件分岐を簡単に実装できます
+ ホールド(押しっぱなし)や画像認識を手軽に使用できます  

[Pythonコマンドの作成](https://github.com/KawaSwitch/Poke-Controller/wiki/%E6%96%B0%E3%81%97%E3%81%84Python%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9)

`self.press(Button.A, 0.1, 1) # Aボタンを押して離す`  
`self.hold([Direction.UP_LEFT, Direction.R_LEFT]) # 左スティックと右スティックを同時にホールド入力`  
`self.isContainTemplate('status.png') # テンプレートマッチング`  
など  

### 画像認識
ポケモン剣盾において便利な画像認識用の機能をメソッドして提供しています  
今後もユーティリティを含めて追加していく予定です  
詳しくは[ここ](https://github.com/KawaSwitch/Poke-Controller/wiki/%E7%94%BB%E5%83%8F%E8%AA%8D%E8%AD%98%E3%81%A8%E3%81%AF)を参照してください  

- 実装済み  
  - テンプレートマッチング  
  - フレーム間差分法(動体検知)  
- 実装予定
  - OCR(文字認識)  
  - 特徴量マッチング  
  - 動体認識  

### コントローラ
"Controller"ボタンを押下すると次のような簡易コントローラが表示されます  
これらのボタンの押下でUSBを繋いだままの移動や操作に使用できます  
またキーボード(コントローラ表示時のみ)でも同様の操作を行うことができます  

現在の簡易コントローラUI  
![簡易コントローラUI](https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/simple_controller_pre_release.PNG)

キーボード操作のキー配置  

| Switchコントローラ | キーボード |
| ---- | ---- |
| A, B, X, Y, L, R | 'a', 'b', ...キー |
| ZL | 'k'キー |
| ZR | 'e'キー |
| MINUS | 'm'キー |
| PLUS | 'p'キー |
| LCLICK | 'q'キー |
| RCLICK | 'w'キー |
| HOME | 'h'キー |
| CAPTURE | 'c'キー |
| 左スティック | 矢印キー |
  
## What you need
[こちら](https://github.com/KawaSwitch/Poke-Controller/wiki)に載せています  

準備物と使用できる機能の表を用意しました  
マイコンのみの場合はGUIによる操作はできません  

|      |  MCUコマンド  | GUIコマンド切替 |   Pythonコマンド<br>(画像認識なし)   |  Pythonコマンド<br>(画像認識あり)  |
| ---- | ---- | ---- | ---- | ---- |
| マイコン  |  〇  |  ×  |  ×  |  ×  |
| 上記+シリアル変換器  |  〇  |  〇  |  〇  |  ×  |
| 上記+キャプチャボード |  〇  |  〇  |  〇  |  〇  |

## How it works
[こちら](https://github.com/KawaSwitch/Poke-Controller/wiki)の下の方に順番で載せています  

上の記事にも同じ画像がありますが実際の接続部分は次のようになります  
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

## License
本プロジェクトではLGPLライセンスのDirectShowLib-2005.dllを同梱し使用しています  
[About DirectShowLib](http://directshownet.sourceforge.net/)  

本プロジェクト自体はMITライセンスです  
See here [LISENCE](https://github.com/KawaSwitch/Poke-Controller/blob/master/LICENSE)  

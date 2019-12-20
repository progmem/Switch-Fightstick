## Fork元: Switch-Fightstick
マイコンをコントローラに偽装してSwitchと通信を行えるようにするプロジェクト  
有名なプロジェクトなので詳しくはそちらのReadmeや解説してくれてるサイトを参照してください  

## Abstract
ポケモン剣盾の自動化ソフトウェア  
マイコンやPythonで書いた自動化コードを抜き差しなくPCで切り替えて操作できます  
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
現バージョンではデバグの効率化/接続用ボタン押下の廃止のために  
一番最初の接続ではコントローラの接続画面からSyncを押してStartする必要があります  
[Poke-Controllerの使い方](https://github.com/KawaSwitch/Poke-Controller/wiki/Poke-Controller%E3%81%AE%E4%BD%BF%E3%81%84%E6%96%B9) ← 準備中  
  
- MCU  
  - A連打  
    その名の通りです  

  - ワット自動化  
    無限ワット対象の巣の200W/2000Wの光は消しておく.   
    レイドのある巣を選ぶ場合倒しておくかレイドの無い巣を選ぶ.  
    またSwitch側の本体設定で「インターネットで時間を合わせる」を**ON**にしておく.  
    
    1: 「ねがいのかたまり」を巣に投げてレポート書いた後, 話しかけずに待機  
    2: .hex書き込み済みのマイコンを接続   
    
    [提供元](https://medaka.5ch.net/test/read.cgi/poke/1574816324/)の>>25を参照  

  - IDくじ&ワット自動化  
    [提供元](https://medaka.5ch.net/test/read.cgi/poke/1574816324/)の>>325を参照  
  
- Python  
  <画像認識なし>  
  - A連打  
    <img src="https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/mash_a.PNG" width="720">
  
  - ワット自動化  
    MCU版の移植  
    MCU版との違いは手順2で代わりにStartを押す.  
    <img src="https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/inifinity_watt_automation.PNG" width="720">

  - IDくじ自動化(ランクマッチバグ使用)  
    ランクマッチに一戦潜る(シングルorダブル)  
    Switch側の本体設定で「インターネットで時間を合わせる」を**OFF**にしておく.  
    
    1: ポケモンセンターの機械(ロトミ)の話しかける位置に立つ  
    2: Startを押す  
    <img src="https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/auto_idLottery.PNG" width="720">
    
  - きのみ自動化(ランクマッチバグ使用)  
    ランクマッチに一戦潜る(シングルorダブル)  
    Switch側の本体設定で「インターネットで時間を合わせる」を**OFF**にしておく.  
    
    1: きのみを収穫したい木の話しかける位置に立つ  
    2: Startを押す  
    <img src="https://github.com/KawaSwitch/Poke-Controller/blob/photo/photos/auto_berry_rankBattle_noImageRecog.PNG" width="720">
    
  <画像認識あり>  
  まだ  


既存のコマンドは順次移植/追加予定で自作も上げていきます  
[プルリクエスト](https://github.com/KawaSwitch/Poke-Controller/pulls)も受け付けています

### コマンドの書き方
必要なコマンドは自分で簡単に書いて追加することができます  
MCUとPythonの双方を選択可能ですがPythonを強く推奨します  
+ 実時間形式で秒を単位として書くことができます
+ ループや条件分岐を簡単に実装できます
+ ホールドや画像認識(予定)を手軽に使用できます  

[Pythonコマンドの作成](https://github.com/KawaSwitch/Poke-Controller/wiki/%E6%96%B0%E3%81%97%E3%81%84Python%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9)

`self.press(Button.A, 0.1, 1)`  
`self.press(Button.UP, 5, 1)`  
など  
  
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
また本プロジェクトでは自動化コード(それ以外でも)のプルリクエスト歓迎してます!  

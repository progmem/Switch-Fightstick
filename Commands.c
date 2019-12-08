#include "Commands.h"

const Command inf_watt_commands[] PROGMEM = {
    { NOP,  	100 },
	{ A,		5 }, // レイドを始める
    { NOP, 		20 },
    { A,		5 },
	{ NOP, 		20 },
    { A,		5 },
    { NOP, 		150 },
    { HOME,		5 },
    { NOP, 		20 },
    { DOWN,		5 },
    { NOP, 		20 },
    { RIGHT, 	5 },
    { NOP, 		20 },
    { RIGHT, 	5 },
    { NOP,  	20 },
    { RIGHT,  	5 },
    { NOP, 		20 },
    { RIGHT,  	5 },
    { NOP,   	20 },
    { A,		5 }, // 設定選択
    { NOP,   	20 },
    { DOWN,   	60 },
    { NOP,   	20 },

    { A,		5 }, // 設定>本体 選択
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 }, // 日付と時刻選択
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
    { UP,	  	5 },
    { NOP,   	20 },
    { RIGHT,	45 },
    { NOP,   	20 },
    { A,		5 }, // OK選択
    { NOP,   	20 },
    { HOME,		5 },
    { NOP,   	20 },
    { HOME,		5 }, // ゲームに戻る
    { NOP,   	30 },
    { B,		5 },
    { NOP,   	50 },
    { A,		5 }, // レイドバトルをいったんやめる
    { NOP,   	20 },
    { NOP,   	150 },// 待機
    { A,		5 },
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
    { B,		5 },
    { NOP,   	20 },
    { B,		5 },
    { NOP,   	20 },
    { NOP,   	150 },// 待機
    
    { HOME,		5 }, // ホームへ
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { RIGHT,	5 },
    { NOP,   	20 },
    { RIGHT, 	5 },
    { NOP,   	20 },
    { RIGHT,	5 },
    { NOP,   	20 },
    { RIGHT,	5 },
    { NOP,   	20 },
    { A,		5 }, // 設定選択
    { NOP,   	20 },
    { DOWN,		60 },

    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 }, // 設定>本体 選択
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 }, // 日付と時刻選択
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
    { HOME,		5 },
    { NOP,   	20 },
    { HOME,		5 }, // ゲームへ
};

const Command inf_id_watt_commands[] PROGMEM = {
	// ワットの回収
	{ A,          5 }, // 巣を選択
	{ NOP,   20 },
	{ A,          5 }, // みんなで　ちょうせん！
	{ NOP,  100 },

	{ HOME,       5 }, // ホームに入る
	{ NOP,   30 },
	{ DOWN,       2 },
	{ NOP,    2 },
	{ RIGHT,     20 },
	{ NOP,    2 },

	{ A,          5 }, // 設定に入る
	{ NOP,   30 },
	{ DOWN,      70 },
	{ NOP,    2 },
	{ A,          5 }, // 本体を選択
	{ NOP,    5 },
	{ DOWN,      20 },
	{ NOP,    2 },

	{ A,          5 }, // 日付と時刻
	{ NOP,    5 },
	{ DOWN,       2 },
	{ NOP,    2 },
	{ DOWN,       2 },
	{ NOP,    2 },
	{ A,          2 }, // 現在の日付と時刻
	{ NOP,    5 },

	{ RIGHT,      2 }, // 日付の変更
	{ NOP,    2 },
	{ RIGHT,      2 },
	{ NOP,    2 },
	{ UP,         2 },
	{ NOP,    2 },
	{ RIGHT,     20 },
	{ A,          5 }, // 日付の決定

	{ HOME,       5 }, // ホームに戻る
	{ NOP,   20 },
	{ A,          5 },
	{ NOP,   30 },
	{ B,          5 },
	{ NOP,   30 },
	{ A,          5 },
	{ NOP,  170 },

	{ A,          2 }, // Wの取得
	{ NOP,    5 },
	{ B,          2 },
	{ NOP,    5 },
	{ B,          2 },
	{ NOP,   15 },
	{ B,          2 },
	{ NOP,   30 },
	{ B,          2 },
	{ NOP,   60 },

	{ X,          5 }, // メニュー
	{ NOP,   30 },
	{ A,          5 }, // タウンマップを開く
	{ NOP,  100 },
	{ UP,         5 },
	{ NOP,    5 },
	{ A,          2 },
	{ NOP,   20 },
	{ A,          2 }, // 移動
	{ NOP,  500 },

	{ PLUS,       5 },

	{ UP,        50 }, // ポケモンセンターに入る
	{ NOP,  100 },
	{ UP,        30 },
	{ UPLEFT,    20 },
	{ NOP,    2 },

	{ A,          2 }, // ロトムに話しかける
	{ NOP,   25 },
	{ A,          2 },
	{ NOP,   25 },
	{ DOWN,       2 },
	{ NOP,   25 },
	{ A,          2 }, // IDくじを選択
	{ NOP,   70 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ A,          2 }, // くじを引く
	{ NOP,  120 },
	{ B,          2 },
	{ NOP,   50 },
	{ B,          2 },
	{ NOP,   70 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,  130 }, // ファーレが鳴る
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 }, // 景品ゲット
	{ NOP,  120 },
	{ B,          2 },
	{ NOP,   25 },
	{ B,          2 },
	{ NOP,   50 },
	{ B,          2 },
	{ NOP,   30 },

	{ DOWNRIGHT, 20 },
	{ DOWN,      40 },
	{ NOP,  100 },

	{ X,          5 },
	{ NOP,   30 },
	{ A,          5 }, // タウンマップを開く
	{ NOP,  100 },
	{ DOWN,       5 },
	{ NOP,    5 },
	{ A,          2 },
	{ NOP,   20 },
	{ A,          2 }, // マップ移動
	{ NOP,  400 },

	{ PLUS,       5 },
	{ NOP,   20 },
	{ UP,       170 }, // 巣への移動
	{ UPLEFT,    65 },
	{ UP,         5 },

};

const int inf_watt_size = sizeof(inf_watt_commands) / sizeof(Command);
const int inf_id_watt_size = sizeof(inf_id_watt_commands) / sizeof(Command);
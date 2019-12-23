#include "Commands.h"

// sync controller with Switch
const Command sync[] PROGMEM = {
	{ NOP,      50 },
	{ A,        2 },
	{ NOP,      200 },
	{ HOME,     2 },
	{ NOP,      50 },
	{ A,        2 },
	{ NOP,      50 },
};
const int sync_size = (int)(sizeof(sync) / sizeof(Command));

// unsync controller from Switch
const Command unsync[] PROGMEM = {
	{ NOP,      50 },
	{ HOME,     2 },
	{ NOP,      20 },
	{ DOWN,		5 },
    { NOP, 		2 },
    { RIGHT, 	2 },
    { NOP, 		5 },
    { RIGHT, 	2 },
    { NOP,  	5 },
    { RIGHT,  	2 },
	{ NOP, 		5 },
	{ A,        5 },
    { NOP, 		60 },
	{ A,        2 },
	{ NOP,      30 },
	{ A,        2 },
	{ NOP,      30 },
};
const int unsync_size = (int)(sizeof(unsync) / sizeof(Command));

// Mashing button A
const Command mash_a_commands[] PROGMEM = {
	{ NOP,      20 },
	{ A,        5 },
};
const int mash_a_size = (int)(sizeof(mash_a_commands) / sizeof(Command));

// Mashing button X (for debug)
const Command mash_x_commands[] PROGMEM = {
	{ NOP,      20 },
	{ X,        5 },
};
const int mash_x_size = (int)(sizeof(mash_x_commands) / sizeof(Command));

// Mashing button X (for debug)
const Command mash_home_commands[] PROGMEM = {
	{ NOP,      20 },
	{ HOME,        5 },
};
const int mash_home_size = (int)(sizeof(mash_home_commands) / sizeof(Command));

// Auto League
const Command auto_league_commands[] PROGMEM = {
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },
	{ NOP,      20 },
	{ A,        5 },

	{ NOP,      20 },
	{ B,        5 },
};
const int auto_league_size = (int)(sizeof(auto_league_commands) / sizeof(Command));

// infinity watt earning
// from: https://medaka.5ch.net/test/read.cgi/poke/1574816324/ >>25
const Command inf_watt_commands[] PROGMEM = {
    { NOP,  	70 },
	{ A,		5 }, // レイドを始める
    { NOP, 		20 },
    { A,		5 },
	{ NOP, 		20 },
    { A,		5 },
    { NOP, 		150 },
    { HOME,		5 },
    { NOP, 		20 },
    { DOWN,		5 },
    { NOP, 		2 },
    { RIGHT, 	2 },
    { NOP, 		5 },
    { RIGHT, 	2 },
    { NOP,  	5 },
    { RIGHT,  	2 },
    { NOP, 		5 },
    { RIGHT,  	2 },
    { NOP,   	5 },
    { A,		5 }, // 設定選択
    { NOP,   	20 },
    { DOWN,   	60 },
    { NOP,   	20 },

    { A,		5 }, // 設定>本体 選択
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { A,		5 }, // 日付と時刻選択
    { NOP,   	10 },
    { A,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
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
    { DOWN,		2 },
    { NOP,   	5 },
    { RIGHT,	2 },
    { NOP,   	5 },
    { RIGHT, 	2 },
    { NOP,   	5 },
    { RIGHT,	2 },
    { NOP,   	5 },
    { RIGHT,	2 },
    { NOP,   	5 },
    { A,		5 }, // 設定選択
    { NOP,   	20 },
    { DOWN,		60 },

    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 }, // 設定>本体 選択
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { DOWN,		5 },
    { NOP,   	10 },
    { A,		5 }, // 日付と時刻選択
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
    { HOME,		5 },
    { NOP,   	20 },
    { HOME,		5 }, // ゲームへ
};

// infinity watt earning and id_lottery
// from: https://medaka.5ch.net/test/read.cgi/poke/1574816324/ >>325
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

const int inf_watt_size = (int)(sizeof(inf_watt_commands) / sizeof(Command));
const int inf_id_watt_size = (int)(sizeof(inf_id_watt_commands) / sizeof(Command));
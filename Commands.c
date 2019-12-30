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

// Mashing button HOME (for debug)
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
const int inf_watt_size = (int)(sizeof(inf_watt_commands) / sizeof(Command));

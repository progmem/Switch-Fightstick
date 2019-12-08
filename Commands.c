#include "Commands.h"

Command inf_watt_commands[] PROGMEM = {
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
    { NOP,   	20 },
    { DOWN,		5 },
    { NOP,   	20 },
    { A,		5 },
    { NOP,   	20 },
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

int inf_watt_size = sizeof(inf_watt_commands) / sizeof(Command);


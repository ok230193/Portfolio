#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<time.h>
#include<stdlib.h>
#include <Windows.h>						
#pragma comment(lib, "winmm.lib")	

int percent(int judge);
int damage_calcu( int offence, int deffence);
int HP_calcu(int *ptr, int HP,int damage);
int critical_hit(int *ptr, int judge,int harm,int gender);

struct ABILITY    /*能力の構造体*/
{
	unsigned char name[41];     /*名前*/
	int gender;                 /*性別*/
	int HP;                     /*HP*/
	int offensive;            /*攻撃力*/
	int defensive;            /*防御力*/
	int fortune;             /*運の良さ*/
	int weapon;                /*武器*/
};

int main(void)
{
	int random = 0;
	int counter = 0;
	int branch = 0;
	int harm = 0;
	int enter = 0;
	

	struct ABILITY character[2]
	= {
		{ /*配列1番目*/
     		NULL,    /*名前*/
			0,       /*性別*/
	    	0,        /*HP*/
		    0,      /*攻撃力*/
			0,      /*防御力*/
			0,      /*運の良さ*/
			0        /*武器*/
		},
		{ /*配列2番目*/
			NULL,    /*名前*/
			0,       /*性別*/
			0,        /*HP*/
			0,      /*攻撃力*/
			0,      /*防御力*/
			0,      /*運の良さ*/
			0        /*武器*/
        }
	};
	
	/*一人目の名前性別入力--------------------------------------------------------------------------------------------------------*/
	
	while (1)                                                                                                                 
	{
		printf("一人目の名前を入力してください【 半角10文字（全角5文字）以上、半角40文字（全角20文字）以内 】\n");  /*1人目名前入力*/
		scanf("%s", &character[0].name[0]);

		if (character[0].name[9] == 0 || character[0].name[40] != 0)  /*半角10文字未満または半角41文字以上の場合再入力*/
		{
			printf("半角10文字（全角5文字）以上、半角40文字（全角20文字）以内で入力してください\n");
		}
		else
		{
			PlaySound(TEXT("system sound1.wav"), NULL, SND_FILENAME);
			printf("性別を入力してください\x1b[31m(半角数字) \x1b[36m 男:1　\x1b[35m 女:2 \x1b[0m\n ");  
			scanf("%d", &character[0].gender);

			/*性別によって声を変える（隠しキャラがいる.......?）*/
			switch(character[0].gender)
			{

			case 1:
				PlaySound(TEXT("man.wav"), NULL, SND_FILENAME);
				break;
             
			case 2:
				PlaySound(TEXT("woman.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character.wav"), NULL, SND_FILENAME);
				break;
			}
				

			break;
		}
	}

	/*-------------------------------------------------------------------------------------------------------------------------*/

	getchar();
	system("cls");


	/*二人目の名前性別入力---------------------------------------------------------------------------------------------------------*/

	while (1)
	{
		printf("二人目の名前を入力してください【 半角10文字（全角5文字）以上、半角40文字（全角20文字）以内 】\n");    /*2人目名前入力*/
		scanf("%s", &character[1].name[0]);

		if (character[1].name[9] == 0 || character[1].name[40] != 0)
		{
			printf("半角10文字（全角5文字）以上、半角40文字（全角20文字）以内で入力してください\n");    /*半角10文字未満または半角41文字以上の場合再入力*/
		}
		else
		{
			PlaySound(TEXT("system sound1.wav"), NULL, SND_FILENAME);
			printf("性別を入力してください\x1b[31m(半角数字) \x1b[36m 男:1　\x1b[35m 女:2 \x1b[0m\n ");
			scanf("%d", &character[1].gender);

			/*性別によって声を変える（隠しキャラがいる.......?）*/
			switch (character[1].gender)
			{

			case 1:
				PlaySound(TEXT("man.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character.wav"), NULL, SND_FILENAME);
				break;

			}
			break;

		}
	}

	system("cls");

	srand(time(NULL));


	for (; counter < 2; counter++)
	{
		/*HPの計算-------------------------------------------------------------------------------------------------------*/

		random = rand() % 4 + 1;
		character[counter].HP = (character[counter].name[1] * random) ;
		character[counter].HP = character[counter].HP % 999 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*攻撃力の計算---------------------------------------------------------------------------------------------------*/

		random = rand() % 4 + 1;
		character[counter].offensive = (character[counter].name[2] + (character[counter].name[3] * random)) % 255 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*防御力の計算---------------------------------------------------------------------------------------------------*/

		random = rand() % 2 + 1;
		character[counter].defensive = (character[counter].name[4] + (character[counter].name[3] * random)) % 127 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*運の良さの計算-------------------------------------------------------------------------------------------------*/

		random = rand() % 16 + 5;
		character[counter].fortune = (character[counter].name[7] * random) % 999 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*武器設定-------------------------------------------------------------------------------------------------------*/

		character[counter].weapon = rand() % 8 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

	}

	/*能力表示-----------------------------------------------------------------------------------------------------------*/

	printf("能力は下記の通り決定した！\n\n");

	for (counter = 0; counter < 2; counter++)
	{
		printf("名前:%s\n", &character[counter].name[0]);
		printf("HP:%d\n", character[counter].HP);
		printf("攻撃力:%d\n", character[counter].offensive);
		printf("防御力:%d\n", character[counter].defensive);
		printf("運の良さ:%d\n", character[counter].fortune);
		printf("\n");
		getchar();
	}


	/*武器表示(武器によって音が出る)*/
    for(counter=0;counter<2;counter++)
	{
		printf("%sの武器は", &character[counter].name[0]);

		switch (character[counter].weapon) 
		{

		case 1: 
			PlaySound(TEXT("rocket launcher.wav"), NULL, SND_FILENAME);
			printf("ロケットランチャー\n");
			break;

		case 2: 
			PlaySound(TEXT("sword.wav"), NULL, SND_FILENAME);
			printf("剣\n"); 
			break;

		case 3:
			PlaySound(TEXT("bow.wav"), NULL, SND_FILENAME);
			printf("弓\n"); 
			break;

		case 4: 
			PlaySound(TEXT("club.wav"), NULL, SND_FILENAME);
			printf("棍棒\n"); 
			break;

		case 5: 
			PlaySound(TEXT("light saber.wav"), NULL, SND_FILENAME);
			printf("ライトセーバー\n");
			break;

		case 6: 
			PlaySound(TEXT("grenade.wav"), NULL, SND_FILENAME);
			printf("手榴弾\n");
			break;

		case 7:
			PlaySound(TEXT("gun.wav"), NULL, SND_FILENAME);
			printf("銃\n"); 
			break;

		case 8:
			PlaySound(TEXT("shuriken.wav"), NULL, SND_FILENAME);
			printf("手裏剣\n");
			break;

		}
		printf("\n");


		getchar();


	}

	system("cls");

	/*-------------------------------------------------------------------------------------------------------------------------*/

	/*攻撃開始------------------------------------------------------------------------------------------------------------------*/

	while (1)
	{
		/*1人目から2人目への攻撃-----------------------------------------------------------------------------------------*/

		printf("%sから%sへの攻撃\n", &character[0].name[0], &character[1].name[0]); 
		printf("%sのHP%d\n\n", &character[1].name[0], character[1].HP);
		printf("enterボタンを２回押して攻撃しよう！！\n");

		branch = percent(character[0].fortune);

		harm = damage_calcu(character[0].offensive, character[1].defensive);

	    switch (character[0].gender)
		{

		case 1:
			PlaySound(TEXT("man attack.wav"), NULL, SND_FILENAME);
			break;

		case 2:
			PlaySound(TEXT("woman attack.wav"), NULL, SND_FILENAME);
			break;

		default:
			PlaySound(TEXT("hidden character attack.wav"), NULL, SND_FILENAME);
			break;

		}

		/*武器表示(武器によって音が出る)*/
		switch (character[0].weapon)
		{

		case 1:
			PlaySound(TEXT("rocket launcher.wav"), NULL, SND_FILENAME);
			break;

		case 2:
			PlaySound(TEXT("sword.wav"), NULL, SND_FILENAME);
			break;

		case 3:
			PlaySound(TEXT("bow.wav"), NULL, SND_FILENAME);
			break;

		case 4:
			PlaySound(TEXT("club.wav"), NULL, SND_FILENAME);
			break;

		case 5:
			PlaySound(TEXT("light saber.wav"), NULL, SND_FILENAME);
			break;

		case 6:
			PlaySound(TEXT("grenade.wav"), NULL, SND_FILENAME);
			break;

		case 7:
			PlaySound(TEXT("gun.wav"), NULL, SND_FILENAME);
			break;

		case 8:
			PlaySound(TEXT("shuriken.wav"), NULL, SND_FILENAME);
			break;

		}

        critical_hit(&harm, branch, harm,character[0].gender);


		/*攻撃が10以下なら攻撃を回避したことにする*/
		if (harm <=10)
		{
			printf("\x1b[0m");
			switch (character[1].gender)
			{

			case 1:
				PlaySound(TEXT("man avoid.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman avoid.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character avoid.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("上手く避けられた！");
		}

		printf("↓%dダメージ\n", harm);

		HP_calcu(&character[1].HP, character[1].HP, harm);

		printf("\x1b[0m");

		if (character[1].HP <= 0)
		{
			character[1].HP = 0;
		}

		printf("%sのHP%d\n", &character[1].name[0],character[1].HP);

		getchar();
		system("cls");


		if (character[1].HP <=0)
		{
			switch (character[1].gender)
			{

			case 1:
				PlaySound(TEXT("man defeat.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman defeat.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character defeat.wav"), NULL, SND_FILENAME);
				break;

			}
			break;
		}

		/*--------------------------------------------------------------------------------------------------------------*/

		/*2人目から1人目への攻撃-----------------------------------------------------------------------------------------*/

		printf("%sから%sへの攻撃\n", &character[1].name[0], &character[0].name[0]);
		printf("%sのHP%d\n\n", &character[0].name[0], character[0].HP);
		printf("enterボタンを２回押して攻撃しよう！！\n");

		branch = percent(character[1].fortune);

		harm = damage_calcu(character[1].offensive, character[0].defensive);

        switch (character[1].gender)
		{

		case 1:
			PlaySound(TEXT("man attack.wav"), NULL, SND_FILENAME);
			break;

		case 2:
			PlaySound(TEXT("woman attack.wav"), NULL, SND_FILENAME);
			break;

		default:
			PlaySound(TEXT("hidden character attack.wav"), NULL, SND_FILENAME);
			break;

		}

		/*武器によって音が出る*/
		switch (character[1].weapon)
		{

		case 1:
			PlaySound(TEXT("rocket launcher.wav"), NULL, SND_FILENAME);
			break;

		case 2:
			PlaySound(TEXT("sword.wav"), NULL, SND_FILENAME);
			break;

		case 3:
			PlaySound(TEXT("bow.wav"), NULL, SND_FILENAME);
			break;

		case 4:
			PlaySound(TEXT("club.wav"), NULL, SND_FILENAME);
			break;

		case 5:
			PlaySound(TEXT("light saber.wav"), NULL, SND_FILENAME);
			break;

		case 6:
			PlaySound(TEXT("grenade.wav"), NULL, SND_FILENAME);
			break;

		case 7:
			PlaySound(TEXT("gun.wav"), NULL, SND_FILENAME);
			break;

		case 8:
			PlaySound(TEXT("shuriken.wav"), NULL, SND_FILENAME);
			break;

		}

		critical_hit(&harm, branch, harm,character[1].gender);


		/*攻撃が10以下なら攻撃を回避したことにする*/
		if (harm <= 10)
		{
			printf("\x1b[0m");
			switch (character[0].gender)
			{

			case 1:
				PlaySound(TEXT("man avoid.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman avoid.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character avoid.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("上手く避けられた！");
		}

		printf("↓%dダメージ\n", harm);

		HP_calcu(&character[0].HP, character[0].HP, harm);

		printf("\x1b[0m");

		if (character[0].HP <= 0)
		{
			character[0].HP = 0;
		}

		printf("%sのHP%d\n", &character[0].name[0],character[0].HP);

		getchar();
		system("cls");

		if (character[0].HP <= 0)
		{
			switch (character[0].gender)
			{

			case 1:
				PlaySound(TEXT("man defeat.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman defeat.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character defeat.wav"), NULL, SND_FILENAME);
				break;

			}

			break;
		}

		/*----------------------------------------------------------------------------------------------------------------*/

	}

	Sleep(1500);

	/*どっちが勝ったかの判定----------------------------------------------------------------------------------------------*/

	if (character[0].HP)
	{
		printf("%sの勝ち！！", &character[0].name[0]);

		switch (character[0].gender)
		{

		case 1:
			PlaySound(TEXT("man win.wav"), NULL, SND_FILENAME);
			if (character[1].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender!=1&&character[1].gender!=2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		case 2:
			PlaySound(TEXT("woman win.wav"), NULL, SND_FILENAME);
			if (character[1].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender != 1 && character[1].gender != 2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		default:
			PlaySound(TEXT("hidden character win.wav"), NULL, SND_FILENAME);
			if (character[1].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[1].gender != 1 && character[1].gender != 2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		}
	}

	if (character[1].HP)
	{
		printf("%sの勝ち！！", &character[1].name[0]);
		switch (character[1].gender)
		{

		case 1:
			PlaySound(TEXT("man win.wav"), NULL, SND_FILENAME);
			if (character[0].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender != 1 && character[0].gender != 2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		case 2:
			PlaySound(TEXT("woman win.wav"), NULL, SND_FILENAME);
			if (character[0].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender != 1 && character[0].gender != 2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		default:
			PlaySound(TEXT("hidden character win.wav"), NULL, SND_FILENAME);
			if (character[0].gender == 1)
			{
				PlaySound(TEXT("man lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender == 2)
			{
				PlaySound(TEXT("woman lose.wav"), NULL, SND_FILENAME);
			}
			if (character[0].gender != 1 && character[0].gender != 2)
			{
				PlaySound(TEXT("hidden character lose.wav"), NULL, SND_FILENAME);
			}
			break;

		}
	}

	/*--------------------------------------------------------------------------------------------------------------------*/

	rewind(stdin);
	getchar();
	return 0;

}

/*main関数終了-----------------------------------------------------------------------------------------------------------------------------------------*/


/*会心の一撃の確率の分岐 関数-------------------------------------*/
int percent(int judge)
{
	int answer = 0;

	if (judge >= 0 && judge <= 100)
	{
		answer = 1;
	}

	if (judge >= 101 && judge <= 300)
	{
		answer = 2;
	}

	if (judge >= 301 && judge <= 600)
	{
		answer = 3;
	}

	if (judge >= 601 && judge <= 800)
	{
		answer = 4;
	}

	if (judge >= 801 && judge <= 999)
	{
		answer = 5;
	}

	rewind(stdin);
	getchar();
	return answer;

}

/*------------------------------------------------------------------*/

/*ダメージ計算関数--------------------------------------------------*/

int damage_calcu(int offensive, int defensive)
{
	int random = 0;
	int harm = 0;
	random = rand();

	harm = offensive - (random % (defensive)+1);

	if (harm <= 0)
	{
		harm = rand() % 5;
	}

	rewind(stdin);
	getchar();
	return harm;

}

/*-------------------------------------------------------------------*/

/*HP計算関数---------------------------------------------------------*/

int HP_calcu(int *ptr, int HP, int damage)
{
	*ptr = HP - damage;

	rewind(stdin);
	getchar();
	return 0;

}

/*-------------------------------------------------------------------*/

/*会心の一撃の関数（会心の一撃かどうかの判定・会心の一撃の際の計算）-*/

int critical_hit(int *ptr, int judge, int harm,int gender)
{
	int random = 0;
	float multi = 0;


	random = rand() % 100 + 1;

	switch (judge)
	{
	case 1:
		if (random <= 2)
		{
			switch (gender)
			{

			case 1:
				PlaySound(TEXT("man special attack.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman spcial attack.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character special attack.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("\x1b[31m");
			printf("会心の一撃だ！\n");
			multi = rand() % 24 + 12;
			multi = multi / 10;
			*ptr = (harm * multi) / 1;
		}
		break;

	case 2:
		if (random <= 5)
		{
			switch (gender)
			{

			case 1:
				PlaySound(TEXT("man special attack.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman special attack.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character special attack.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("\x1b[31m");
			printf("会心の一撃だ！\n");
			multi = rand() % 24 + 12;
			multi = multi / 10;
			*ptr = (harm * multi) / 1;
		}
		break;

	case 3:
		if (random <= 10)
		{
			switch (gender)
			{

			case 1:
				PlaySound(TEXT("man special attack.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman special attack.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character special attack.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("\x1b[31m");
			printf("会心の一撃だ！\n");
			multi = rand() % 24 + 12;
			multi = multi / 10;
			*ptr = (harm * multi) / 1;
		}
		break;

	case 4:
		if (random <= 25)
		{
			switch (gender)
			{

			case 1:
				PlaySound(TEXT("man special attack.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman special attack.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character special attack.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("\x1b[31m");
			printf("会心の一撃だ！\n");
			multi = rand() % 24 + 12;
			multi = multi / 10;
			*ptr = (harm * multi) / 1;
		}
		break;

	case 5:
		if (random <= 40)
		{
			switch (gender)
			{

			case 1:
				PlaySound(TEXT("man special attack.wav"), NULL, SND_FILENAME);
				break;

			case 2:
				PlaySound(TEXT("woman special attack.wav"), NULL, SND_FILENAME);
				break;

			default:
				PlaySound(TEXT("hidden character special attack.wav"), NULL, SND_FILENAME);
				break;

			}
			printf("\x1b[31m");
			printf("会心の一撃だ！\n");
			multi = rand() % 24 + 12;
			multi = multi / 10;
			*ptr = (harm * multi) / 1;

		}
		break;

	}

	rewind(stdin);
	getchar();
	return 0;

}

/*-------------------------------------------------------------------*/
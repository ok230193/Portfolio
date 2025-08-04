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

struct ABILITY    /*�\�͂̍\����*/
{
	unsigned char name[41];     /*���O*/
	int gender;                 /*����*/
	int HP;                     /*HP*/
	int offensive;            /*�U����*/
	int defensive;            /*�h���*/
	int fortune;             /*�^�̗ǂ�*/
	int weapon;                /*����*/
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
		{ /*�z��1�Ԗ�*/
     		NULL,    /*���O*/
			0,       /*����*/
	    	0,        /*HP*/
		    0,      /*�U����*/
			0,      /*�h���*/
			0,      /*�^�̗ǂ�*/
			0        /*����*/
		},
		{ /*�z��2�Ԗ�*/
			NULL,    /*���O*/
			0,       /*����*/
			0,        /*HP*/
			0,      /*�U����*/
			0,      /*�h���*/
			0,      /*�^�̗ǂ�*/
			0        /*����*/
        }
	};
	
	/*��l�ڂ̖��O���ʓ���--------------------------------------------------------------------------------------------------------*/
	
	while (1)                                                                                                                 
	{
		printf("��l�ڂ̖��O����͂��Ă��������y ���p10�����i�S�p5�����j�ȏ�A���p40�����i�S�p20�����j�ȓ� �z\n");  /*1�l�ږ��O����*/
		scanf("%s", &character[0].name[0]);

		if (character[0].name[9] == 0 || character[0].name[40] != 0)  /*���p10���������܂��͔��p41�����ȏ�̏ꍇ�ē���*/
		{
			printf("���p10�����i�S�p5�����j�ȏ�A���p40�����i�S�p20�����j�ȓ��œ��͂��Ă�������\n");
		}
		else
		{
			PlaySound(TEXT("system sound1.wav"), NULL, SND_FILENAME);
			printf("���ʂ���͂��Ă�������\x1b[31m(���p����) \x1b[36m �j:1�@\x1b[35m ��:2 \x1b[0m\n ");  
			scanf("%d", &character[0].gender);

			/*���ʂɂ���Đ���ς���i�B���L����������.......?�j*/
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


	/*��l�ڂ̖��O���ʓ���---------------------------------------------------------------------------------------------------------*/

	while (1)
	{
		printf("��l�ڂ̖��O����͂��Ă��������y ���p10�����i�S�p5�����j�ȏ�A���p40�����i�S�p20�����j�ȓ� �z\n");    /*2�l�ږ��O����*/
		scanf("%s", &character[1].name[0]);

		if (character[1].name[9] == 0 || character[1].name[40] != 0)
		{
			printf("���p10�����i�S�p5�����j�ȏ�A���p40�����i�S�p20�����j�ȓ��œ��͂��Ă�������\n");    /*���p10���������܂��͔��p41�����ȏ�̏ꍇ�ē���*/
		}
		else
		{
			PlaySound(TEXT("system sound1.wav"), NULL, SND_FILENAME);
			printf("���ʂ���͂��Ă�������\x1b[31m(���p����) \x1b[36m �j:1�@\x1b[35m ��:2 \x1b[0m\n ");
			scanf("%d", &character[1].gender);

			/*���ʂɂ���Đ���ς���i�B���L����������.......?�j*/
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
		/*HP�̌v�Z-------------------------------------------------------------------------------------------------------*/

		random = rand() % 4 + 1;
		character[counter].HP = (character[counter].name[1] * random) ;
		character[counter].HP = character[counter].HP % 999 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*�U���͂̌v�Z---------------------------------------------------------------------------------------------------*/

		random = rand() % 4 + 1;
		character[counter].offensive = (character[counter].name[2] + (character[counter].name[3] * random)) % 255 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*�h��͂̌v�Z---------------------------------------------------------------------------------------------------*/

		random = rand() % 2 + 1;
		character[counter].defensive = (character[counter].name[4] + (character[counter].name[3] * random)) % 127 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*�^�̗ǂ��̌v�Z-------------------------------------------------------------------------------------------------*/

		random = rand() % 16 + 5;
		character[counter].fortune = (character[counter].name[7] * random) % 999 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

		/*����ݒ�-------------------------------------------------------------------------------------------------------*/

		character[counter].weapon = rand() % 8 + 1;

		/*---------------------------------------------------------------------------------------------------------------*/

	}

	/*�\�͕\��-----------------------------------------------------------------------------------------------------------*/

	printf("�\�͉͂��L�̒ʂ茈�肵���I\n\n");

	for (counter = 0; counter < 2; counter++)
	{
		printf("���O:%s\n", &character[counter].name[0]);
		printf("HP:%d\n", character[counter].HP);
		printf("�U����:%d\n", character[counter].offensive);
		printf("�h���:%d\n", character[counter].defensive);
		printf("�^�̗ǂ�:%d\n", character[counter].fortune);
		printf("\n");
		getchar();
	}


	/*����\��(����ɂ���ĉ����o��)*/
    for(counter=0;counter<2;counter++)
	{
		printf("%s�̕����", &character[counter].name[0]);

		switch (character[counter].weapon) 
		{

		case 1: 
			PlaySound(TEXT("rocket launcher.wav"), NULL, SND_FILENAME);
			printf("���P�b�g�����`���[\n");
			break;

		case 2: 
			PlaySound(TEXT("sword.wav"), NULL, SND_FILENAME);
			printf("��\n"); 
			break;

		case 3:
			PlaySound(TEXT("bow.wav"), NULL, SND_FILENAME);
			printf("�|\n"); 
			break;

		case 4: 
			PlaySound(TEXT("club.wav"), NULL, SND_FILENAME);
			printf("���_\n"); 
			break;

		case 5: 
			PlaySound(TEXT("light saber.wav"), NULL, SND_FILENAME);
			printf("���C�g�Z�[�o�[\n");
			break;

		case 6: 
			PlaySound(TEXT("grenade.wav"), NULL, SND_FILENAME);
			printf("��֒e\n");
			break;

		case 7:
			PlaySound(TEXT("gun.wav"), NULL, SND_FILENAME);
			printf("�e\n"); 
			break;

		case 8:
			PlaySound(TEXT("shuriken.wav"), NULL, SND_FILENAME);
			printf("�藠��\n");
			break;

		}
		printf("\n");


		getchar();


	}

	system("cls");

	/*-------------------------------------------------------------------------------------------------------------------------*/

	/*�U���J�n------------------------------------------------------------------------------------------------------------------*/

	while (1)
	{
		/*1�l�ڂ���2�l�ڂւ̍U��-----------------------------------------------------------------------------------------*/

		printf("%s����%s�ւ̍U��\n", &character[0].name[0], &character[1].name[0]); 
		printf("%s��HP%d\n\n", &character[1].name[0], character[1].HP);
		printf("enter�{�^�����Q�񉟂��čU�����悤�I�I\n");

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

		/*����\��(����ɂ���ĉ����o��)*/
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


		/*�U����10�ȉ��Ȃ�U��������������Ƃɂ���*/
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
			printf("��肭������ꂽ�I");
		}

		printf("��%d�_���[�W\n", harm);

		HP_calcu(&character[1].HP, character[1].HP, harm);

		printf("\x1b[0m");

		if (character[1].HP <= 0)
		{
			character[1].HP = 0;
		}

		printf("%s��HP%d\n", &character[1].name[0],character[1].HP);

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

		/*2�l�ڂ���1�l�ڂւ̍U��-----------------------------------------------------------------------------------------*/

		printf("%s����%s�ւ̍U��\n", &character[1].name[0], &character[0].name[0]);
		printf("%s��HP%d\n\n", &character[0].name[0], character[0].HP);
		printf("enter�{�^�����Q�񉟂��čU�����悤�I�I\n");

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

		/*����ɂ���ĉ����o��*/
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


		/*�U����10�ȉ��Ȃ�U��������������Ƃɂ���*/
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
			printf("��肭������ꂽ�I");
		}

		printf("��%d�_���[�W\n", harm);

		HP_calcu(&character[0].HP, character[0].HP, harm);

		printf("\x1b[0m");

		if (character[0].HP <= 0)
		{
			character[0].HP = 0;
		}

		printf("%s��HP%d\n", &character[0].name[0],character[0].HP);

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

	/*�ǂ��������������̔���----------------------------------------------------------------------------------------------*/

	if (character[0].HP)
	{
		printf("%s�̏����I�I", &character[0].name[0]);

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
		printf("%s�̏����I�I", &character[1].name[0]);
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

/*main�֐��I��-----------------------------------------------------------------------------------------------------------------------------------------*/


/*��S�̈ꌂ�̊m���̕��� �֐�-------------------------------------*/
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

/*�_���[�W�v�Z�֐�--------------------------------------------------*/

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

/*HP�v�Z�֐�---------------------------------------------------------*/

int HP_calcu(int *ptr, int HP, int damage)
{
	*ptr = HP - damage;

	rewind(stdin);
	getchar();
	return 0;

}

/*-------------------------------------------------------------------*/

/*��S�̈ꌂ�̊֐��i��S�̈ꌂ���ǂ����̔���E��S�̈ꌂ�̍ۂ̌v�Z�j-*/

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
			printf("��S�̈ꌂ���I\n");
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
			printf("��S�̈ꌂ���I\n");
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
			printf("��S�̈ꌂ���I\n");
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
			printf("��S�̈ꌂ���I\n");
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
			printf("��S�̈ꌂ���I\n");
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
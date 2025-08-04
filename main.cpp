#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<time.h>
#include<stdlib.h>

int main(void)
{
	int iBox[10];
	int iCounter = 0;
	int iCounter2 = 1;
	int iCounter3 = 0;
	int iTem = 0;

	srand(time(NULL));
	
	for (; iCounter < 10; iCounter++)
	{
		iBox[iCounter] = ((rand() % 1001) + 1);
	}

		for (iCounter = 0; iCounter < 10; iCounter++)
		{
			printf("%d\n", iBox[iCounter]);
		}


		for (; iCounter3 <= 10; iCounter3++,iCounter=0,iCounter2=1)
		{
			for (iCounter = 0; iCounter2 < 10; iCounter++, iCounter2++)
			{

				if (iBox[iCounter] >= iBox[iCounter2])
				{
					iTem = iBox[iCounter];
					iBox[iCounter] = iBox[iCounter2];
					iBox[iCounter2] = iTem;
				}

			}

		}

	for (iCounter = 0; iCounter < 10; iCounter++)
	{
		printf("”z—ñ%d”Ô–Ú‚Í%d\n", iCounter, iBox[iCounter]);
	}

	rewind(stdin);
	getchar();
	return 0;

}
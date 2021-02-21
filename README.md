#include<stdio.h>
#include<string.h>
#define for0(i,n) for(int i = 0; i < n; ++i)

typedef struct {
	char city[20];
	char std[10];
} Cities;

void linearSearch(Cities CS[],int n){
	char name[20];
	printf("Enter the city name to search : ");
	scanf("%s",name);
	for0(i,n){
		if(strcmp(name,CS[i].city)==0){
			printf("\n%s %s\n\n",CS[i].city, CS[i].std);
			return;
		}
	}
	printf("\nCity not in the list\n\n");
}

void sortStruct(Cities pA[],int i){
		for0(j,i){
		for0(k,i-j-1){
			if(strcmp(pA[k].city,pA[k+1].city)>0){
				Cities temp = pA[k];
				pA[k] = pA[k+1];
				pA[k+1] = temp;
			}
		}	
	}
}

void binarySearch(Cities CS[],int n){
	char name[20];
	printf("Enter the city name to search : ");
	scanf("%s",name);
		sortStruct(CS,n);
		// for0(i,n){
		// printf("%d. %s %s\n",i,CS[i].city,CS[i].std);	
		// }
		int low = 0, high = n-1;
		while(low <= high){
			int mid = (low+high)/2;
			if(strcmp(CS[mid].city,name)==0){
			printf("\n%s %s\n\n",CS[mid].city, CS[mid].std);
			return;
			}
			else if(strcmp(CS[mid].city,name)>0){
				high = mid - 1;
			}
			else low = mid + 1;
		}
		printf("\nCity not in the list\n\n");
}

int main(){
	Cities CS[100];
	FILE *fp = fopen("file.txt","r");
	if(fp == NULL){
		printf("Error! file did not open.");
		return 0;
	}

	int n = 0;
	while(feof(fp)==0){
		fscanf(fp,"%s %s",CS[n].city,CS[n].std);
		printf("%d. %s %s\n",n,CS[n].city,CS[n].std);
		++n;
	}

	char name[20];
	int ch;
	do{
		printf("Enter \n1 to search using linear search\n2 to search using binary search\n3 to quit\n");
		scanf("%d",&ch);
		if(ch == 3 ){
			printf("\nQUIT\n");
			return 0;
		}
		switch(ch) {
			case 1 : linearSearch(CS,n-1);break;
			case 2 : binarySearch(CS,n-1);break;
			default : printf("\nWrong option\n\n");
		}
	}while(1);
}

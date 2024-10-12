#include <iostream>
#include <string>
#include <vector>
#include <string.h>
#include <cstdint>
#include <cstdio>
#include <iomanip>
#include <sys/mman.h>
#include <unistd.h>

#define STR_SZ 0x50
#define MAX_ALLOCS 0x4
#define BUF_SZ 0x3000

using namespace std;

class Animal{
	public:
		Animal():name(NULL), weight(0){}

		Animal(string name, uint64_t weight, string msg){
			this->name = new char[name.length()+1];
			strcpy(this->name, name.c_str());
			this->weight = weight;
			this->sound = msg;
		}

		virtual void showInfo(){
			cout << "Name: " << name << endl;
			cout << "Weight: " << weight << endl;
		}
		
		virtual void makeSound(){
			cout << type << " makes a sound << " << sound << " >>" << endl;
		}

		virtual ~Animal(){
			type.clear();
			sound.clear();
			delete[] name;
		}
	
	public:
		char *name;
		uint64_t id;
		string type;
	protected:
		uint64_t weight;
		string sound;
};

class Monke :public Animal{
	public:
		Monke():age(0){}
		Monke(string name, uint64_t weight, string msg, uint64_t age){
			this->type = "Monke";
			this->name = new char[name.length()+1];
			strcpy(this->name, name.c_str());
			this->weight = weight;
			this->sound = msg;
			this->age = age;
			this->id = (classId)++;
		}

		void showInfo(){
			cout << "Monke ID: " << id << endl;
			cout << "Monke name: " << name << endl;
			cout << "Monke age: " << age << endl;
			cout << "Monke weight: " << weight << endl;
		}

		~Monke(){
			classId--;
			age = 0;
		}
	
	private:
		static uint64_t classId;
		uint64_t age;
};

class Cat :public Animal{
	public:
		Cat():furs(0){}

		Cat(string name, uint64_t weight, string msg, uint64_t furs){
			this->type = "Cat";
			this->name = new char[name.length()+1];
			strcpy(this->name, name.c_str());
			this->weight = weight;
			this->sound = msg;
			this->furs = furs;
			this->id = (classId)++;
		}

		void showInfo(){
			cout << "Cat ID: " << id <<endl;
			cout << "Cat name: " << name <<endl;
			cout << "Cat weight: " << weight <<endl;
			cout << "Cat furcount: " << furs <<endl;
		}
		
		~Cat(){
			classId--;
			furs = 0;
		}
	
	private:
		static uint64_t classId;
		uint64_t furs;
};

vector<Animal*> animalList;
uint64_t Monke::classId = 0;
uint64_t Cat::classId = 0;
char *globalbuf;

size_t getstr(size_t sz){
    cout << ">> ";
    size_t recv = 0;
    while(recv < sz && recv < BUF_SZ){
        if(read(STDIN_FILENO, &globalbuf[recv], 1) < 0) exit(-1);
        if(globalbuf[recv] == '\n'){
            globalbuf[recv] = '\0';
            return recv;
        }
        recv++;
    }
	return 0;
}

void animaltypes(){
	cout << "We currently only have 2 animal types" << endl;
	cout << "1. Monke" << endl;
	cout << "2. Cat" << endl;
}

void addMenu(){
	unsigned int choice, weight;
	string name, sound;
	if(animalList.size() >= MAX_ALLOCS){
		cout << "Data is full!" << endl;
		return;
	}
	animaltypes();
	cout << ">> ";
	cin >> choice;
	cin.ignore();

	cout << "Name: ";
	cin >> setw(STR_SZ) >> name;
 	cout << "Sound: ";
	cin >> setw(STR_SZ) >> sound;
	cout << "Weight: ";
	cin >> weight;

	switch(choice){
		case 1:
			uint64_t age;
			cout << "Age: ";
			cin >> age;
			animalList.push_back(new Monke(name, weight, sound, age));
			break;
		case 2:
			uint64_t furs;
			cout << "How many furs(num): ";
			cin >> furs;
			animalList.push_back(new Cat(name, weight, sound, furs));
			break;
		default: cout << "No such animal"; break;
	}
}

void listAnimal(){
	cout << "=========== Monke =============" << endl;
    for (auto& animal : animalList) {
		if(animal->type == "Monke"){
			animal->showInfo();
			cout << "===============================" << endl;
		}
    }
	cout << ">>>=========================<<<" << endl;

	cout << "===========  Cat  =============" << endl;
    for (auto& animal : animalList) {
		if(animal->type == "Cat"){
			animal->showInfo();
			cout << "===============================" << endl;
		}
	}
}

void hearSound(){
	uint64_t choice;
	string type;
	uint64_t id;
	cout << "What kind of animal would you like to hear?" <<endl;
	cout << "1. Monke" <<endl;
	cout << "2. Cat" <<endl;
	cout << ">> ";
	cin >> choice;
	cout << "Which id?" <<endl;
	cout << ">> ";
	cin >> id;
	switch(choice){
		case 1:
			for(auto& animal: animalList){
				if(animal->type == "Monke" && animal->id == id){
					animal->makeSound();
				}
			}
			break;
		case 2:
			for(auto& animal: animalList){
				if(animal->type == "Cat" && animal->id == id){
					animal->makeSound();
				}
			}
			break;
		default: cout << "No such animal" << endl;
	}
}

void editName(){
	uint64_t choice;
	size_t recv;
	uint64_t id;
	cout << "What kind of animal would you like to edit?" <<endl;
	cout << "1. Monke" << endl;
	cout << "2. Cat" << endl;
	cout << ">> ";
	cin >> choice;
	cout << "Which id?" << endl;
	cout << ">> ";
	cin >> id;
	cout << "What's the new name?" << endl;
	recv = getstr(STR_SZ);
	switch(choice){
		case 1:
			for(auto& animal: animalList){
				if(animal->type == "Monke" && animal->id == id){
					memcpy(animal->name, globalbuf, recv);
				}
			}
			break;
		case 2:
			for(auto& animal: animalList){
				if(animal->type == "Cat" && animal->id == id){
					memcpy(animal->name, globalbuf, recv);
				}
			}
			break;
		default: cout << "No such animal" << endl;
	}
}

void printMenu(){
	cout << "Welcome to KaZooYa" << endl;
	cout << "The Online Zoo Management Tool" << endl;
	cout << "You, as the managing director of KaZooya are tasked to oversee the Animals in the Zoo" << endl;
	cout << "You can only manage up to " << MAX_ALLOCS << " animals" << endl;
	cout << "Now, what would you like to do?" << endl;
	cout << "1. Add new animal" << endl;
	cout << "2. Show animal list" << endl;
	cout << "3. Hear animal sound" << endl;
	cout << "4. Edit animal name" << endl;
	cout << "5. Feedback" << endl;
	cout << "6. Done for the day" << endl;
}

void feedback(){
	cout << "We are by no means perfect, please provide some feedbacks for future improvements!" << endl;
	getstr(0x30);
}

void init(){
	animalList.reserve(MAX_ALLOCS);
	globalbuf = (char*) mmap(NULL, BUF_SZ, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (globalbuf == MAP_FAILED){
        puts("Mmap failed");
        exit(EXIT_FAILURE);
    }
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void){
	init();
	unsigned int choice = 0;
	cout << "Your buf is at: " << (void*)globalbuf << endl;
	for(;;){
		printMenu();
		cout << ">> ";
		cin >> choice;
		switch(choice){
			case 1: addMenu(); break;
			case 2:
				if(animalList.empty()){
					cout << "... The zoo is empty" << endl;
				}else{
					listAnimal();
				}
				break;
			case 3:
				if(animalList.empty()){
					cout << "... The zoo is empty" << endl;
				}else{
					hearSound();
				}
				break;
			case 4:
				if(animalList.empty()){
					cout << "... The zoo is empty" << endl;
				}else{
					editName();
				}
				break;
			case 5: feedback(); break;
			case 6: exit(1); break;
			default: cout << "Did you mash your keyboard?" << endl;
		}
	}
	return 0;
}
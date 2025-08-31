#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>

#define MAX_WORKERS 8

class Worker {
public:
    Worker() {}
    virtual void work(void) const {
        std::cout << "Ughh... I hate this job" << std::endl;
    }
    ~Worker() = default;
};

class Admin : public Worker {
public:
    Admin() : Worker() {}
    Admin(std::string name) : m_name(name) {}
    void work(void) const override {
        std::cout << this->m_name << ": I have a name because I'm special!" << std::endl;
    }

private:
    std::string m_name{};
};

Worker *workers[MAX_WORKERS] = { nullptr };
std::vector<int> choice_history;
static const std::vector<std::string> choice_map = {
    "Hired a worker",
    "Fired a worker",
    "Tired out a worker",
    "Viewed history",
    "Cleared history"
};

void setup(void) {
    Admin admin{};
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void) {
    system("/bin/sh");
}

int menu(void) {
    int input;
    std::cout << "1. Hire\n"
                << "2. Fire\n"
                << "3. Tire\n"
                << "4. View History\n"
                << "5. Clear History\n"
                << "6. Exit\n"
                << ">> ";
    std::cin >> input;
    return input;
}

int get_index(void) {
    int i;
    std::cout << "Which index?\n>> ";
    std::cin >> i;
    if (i < 0 || i > MAX_WORKERS) {
        std::cout << "You don't have that many workers!\n";
        exit(1);
    }
    return i;
}

void hire(void) {
    int i = get_index();
    workers[i] = new Worker();
}

void fire(void) {
    int i = get_index();
    if (workers[i] != 0) {
        delete workers[i];
        workers[i] = nullptr;
    }
}

void tire(void) {
    int i = get_index();
    if (workers[i] != 0) {
        workers[i]->work();
    }
}

void view_history(void) {
    std::cout << "So far, you have:\n";
    for (int choice : choice_history) {
        std::string choice_text;
        if (choice <= choice_map.size()) {
            choice_text = choice_map[choice - 1];
        } else {
            choice_text = "UNKNOWN";
        }

        std::cout << "- " << choice_text << " (" << choice << ")\n";
    }
}

int main() {
    int choice = 0;
    setup();
    do {
        choice = menu();
        choice_history.push_back(choice);
        switch (choice) {
            case 1:
                hire();
                break;
            case 2:
                fire();
                break;
            case 3:
                tire();
                break;
            case 4:
                view_history();
                break;
            case 5:
                choice_history.clear();
                break;
            case 6:
                break;
            default:
                std::cout << "Invalid choice!" << std::endl;
        }
    } while (choice != 6);

    return 0;
}
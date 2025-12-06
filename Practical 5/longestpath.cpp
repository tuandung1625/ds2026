#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <climits>

using namespace std;

void run_mapper() {
    string path;
    while (getline(cin, path)) {
        int length = path.length();
        cout << "1" << "\t" << length << endl;
    }
}

void run_reducer() {
    string line;
    int max_length = 0;
    string key;
    int length;

    while (getline(cin, line)) {
        stringstream ss(line);
        ss >> key >> length;

        if (length > max_length) {
            max_length = length;
        }
    }

    cout << max_length << "\t" << 1 << endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <mapper | reducer>" << endl;
        return 1;
    }

    string mode = argv[1];
    if (mode == "mapper") {
        run_mapper();
    } else if (mode == "reducer") {
        run_reducer();
    } else {
        cerr << "Invalide mode: " << mode << ". Use 'mapper' or 'reducer'." << endl;
        return 1;
    }

    return 0;
}
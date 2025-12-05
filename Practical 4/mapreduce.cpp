#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <map>
#include <algorithm>
#include <vector>

using namespace std;

// Remove all non-alphanumeric characters and normalize all letters.
string normalize(const string& word) {
    string result = word;
    
    result.erase(remove_if(result.begin(), result.end(), [](char c){
        return !isalnum(c);
    }), result.end());

    transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

void run_mapper() {
    string line;
    while (getline(cin, line)) {
        stringstream ss(line);
        string word;
        while (ss >> word) {
            string normalized_word = normalize(word);
            if (!normalized_word.empty()) {
                cout << normalized_word << "\t" << 1 << endl;
            }
        }
    }
}

void run_reducer() {
    string line;
    string current_word = "";
    int current_count = 0;

    // Receive <input, 1> from run_mapper()
    while (getline(cin, line)) {
        stringstream ss(line);
        string word;
        int count;

        ss >> word >> count;

        if (word != current_word) {
            if (!current_word.empty()) {
                cout << current_word << "\t" << current_count << endl;
            }

            current_word = word;
            current_count = count;
        } else {
            current_count += count;
        }
    }

    // Print the result for each word
    if (!current_word.empty()) {
        cout << current_word << "\t" << current_count << endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <mapper|reducer>" << endl;
        return 1;
    }

    string mode = argv[1];
    if (mode == "mapper") {
        run_mapper();
    } else if (mode == "reducer") {
        run_reducer();
    } else {
        cerr << "Invalid mode: " << mode << ". Use 'mapper' or 'reducer'." << endl;
        return 1;
    }

    return 0;
}
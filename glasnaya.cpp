#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    int cnt = 0;
    for (char c : s)
        if (string("aeiouAEIOU").find(c) != string::npos)
            ++cnt;
    cout << "Vowels: " << cnt << endl;
    return 0;
}

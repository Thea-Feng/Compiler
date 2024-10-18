#include <cstddef>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <memory>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <stack>
#include <unordered_set>
using namespace std;

struct Rule {
    string lhs;
    vector<string> rhs;
};
map<string, unordered_set<string> > FIRST, FOLLOW;
map<string, bool> NULLABLE;
unordered_set<string> NonTerminal, Terminal;
map<string, map<string, int> > ParseTable;
bool isTerminal(string s) {
    return NonTerminal.find(s) == NonTerminal.end();
}
vector<string> readFromCode(const string& filename){
    ifstream file(filename);
    vector<string> results;
    string line;
    getline(file, line);
    istringstream iss(line);
    string element;
    while(getline(iss, element, ' ')){
        if(element == "comment") continue;
        results.push_back(element);
    }
    // while (getline(file, line)) {
    //     string element1, element2;
    //     int pos = 0;
    //     while(line[pos] != ' ')pos++;
    //     element1 = line.substr(0, pos);
    //     element2 = line.substr(pos+1);
    //     if(element1 == "COMMENT") continue;
    //     results.push_back(element1);
    //     results.push_back(element2);

    // }
    return results;
}

vector<Rule> readFromFile(const string& filename) {
    ifstream file(filename);
    vector<Rule> results;
    Rule ini;
    ini.lhs = "S";
    ini.rhs.push_back("prog");
    ini.rhs.push_back("$");
    results.push_back(ini);
    Terminal.insert("$");
    string line;
    while (getline(file, line)) {
        Rule a;
        istringstream iss(line);
        string element;
        getline(iss, element, ' ');
        if(element == "") continue;
        a.lhs = element;
        NULLABLE[element] = false;
        if(isTerminal(element))
            Terminal.insert(element);
        while (getline(iss, element, ' ')) {
            if(element != "::=") {
                a.rhs.push_back(element);
                NULLABLE[element] = false;
                if(isTerminal(element))
                    Terminal.insert(element);
            }  
        }
        results.push_back(a);
    }
    return results;
}

string token_str_to_name(string token_str) {
        /* Reserved Keywords */
        if(token_str =="null")       return "NULL";
        if(token_str =="true")      return "TRUE";
        if(token_str =="false")     return "FALSE";
        if(token_str =="void")     return "TVOID";
        if(token_str =="int")      return "TINT";
        if(token_str =="string")   return "TSTRING";
        if(token_str =="bool")     return "TBOOL";
        if(token_str =="if")        return "IF";
        if(token_str =="else")      return "ELSE";
        if(token_str =="while")     return "WHILE";
        if(token_str =="for")       return "FOR";
        if(token_str =="return")    return "RETURN";
        if(token_str =="new")       return "NEW";
        /* Punctuations */
        if(token_str ==";") return "SEMICOLON";
        if(token_str ==",")     return "COMMA";
        if(token_str =="{")    return "LBRACE";
        if(token_str =="}")    return "RBRACE";
        if(token_str =="(")    return "LPAREN";
        if(token_str ==")")    return "RPAREN";
        if(token_str =="[")  return "LBRACKET";
        if(token_str =="]")  return "RBRACKET";
        /* Binary Operators */
        if(token_str =="*")      return "STAR";
        if(token_str =="+")      return "PLUS";
        if(token_str =="-")     return "MINUS";
        if(token_str =="<<")    return "LSHIFT";
        if(token_str ==">>")   return "RLSHIFT";
        if(token_str ==">>>")   return "RASHIFT";
        if(token_str =="<")      return "LESS";
        if(token_str =="<=")    return "LESSEQ";
        if(token_str ==">")     return "GREAT";
        if(token_str ==">=")   return "GREATEQ";
        if(token_str =="==")        return "EQ";
        if(token_str =="!=")       return "NEQ";
        if(token_str =="&")      return "LAND";
        if(token_str =="|")       return "LOR";
        if(token_str =="[&]")      return "BAND";
        if(token_str =="[|]")       return "BOR";
        /* Unary Operators */
        if(token_str =="!")       return "NOT";
        if(token_str =="~")     return "TILDE";
        /* Other Token Classes */
        if(token_str =="=")    return "ASSIGN";
        if(token_str =="intliteral")return "INTLITERAL";
        if(token_str =="id")        return "ID";
        if(token_str =="stringliteral")
                        return "STRINGLITERAL";
        if(token_str =="var")       return "VAR";
        if(token_str =="global")    return "GLOBAL";
        if(token_str == "$") return "EOF";
        return "Invalid";
}


bool setUnion(unordered_set<string>& a, const unordered_set<string>& b){
    int sz = a.size();
    for(auto s: b) 
        a.insert(s);
    return a.size() != sz;
}
void init(){
   NonTerminal= {
    "S", "arg", "args", "args'", "arr_idx", "assign", "block", "bop", "decl", "else_body", "else_stmt", "exp", "exp'", "exp_opt", "exps", "exps'", "fdecl", "func_call", "gdecl", "gexp", "gexps", "gexps'", "if_stmt", "primary", "primary_t", "prog", "stmt", "stmt'", "stmts", "t", "t_arr", "term", "uop", "vdecl", "vdecls"
    };

    // NonTerminal = {"S", "prog", "decl", "gdecl", "fdecl", "vdecls", "vdecls'", "vdecl", "args", "args'", "arg", "block", "t", "t_arr", "primary_t", "gexps", "gexps'", "gexp", "stmts", "stmt", "stmt'", "lhs_idx", "stmt_opt", "exp_opt", "if_stmt", "else_stmt", "else_body", "exps", "exps'", "exp", "exp_30", "exp_30'", "exp_40", "exp_40'", "exp_50", "exp_50'", "exp_60", "exp_60'", "exp_70", "exp_70'", "exp_80", "exp_80'", "exp_90", "exp_90'", "exp_100", "exp_100'", "bop_100", "bop_90", "bop_80", "bop_70", "bop_60", "bop_50", "bop_40", "bop_30", "bop_30'", "term", "primary", "id'", "uop", "''"};
}
int main(int argc, char const *argv[]) {
    if (argc == 3) {
        string file1 = argv[1];
        string file2 = argv[2];
        init();
        vector<Rule> rules = readFromFile(file1);
        // for(auto& a : rules){
        //     cout << "lhs: " << a.lhs << ", rhs: ";
        //     for(auto& s : a.rhs){
        //         cout << s << "#";
        //     }
        //     cout << "\n";
        // }
        for (auto& rule: rules){
            for (auto element: rule.rhs)
                    if(element == "''") 
                        NULLABLE[rule.lhs] = true;
        }

        for (string Z: Terminal)
            FIRST[Z] = {Z};
        bool change = true;
        printf("nontern size %d term size %d\n", NonTerminal.size(), Terminal.size());
        // construct FIRST FOLLOW SET
        int cnt = 0;
        while(change){
            cnt++;
            change = false;
            FOLLOW["S"] = {"$"}; 

            for (auto rule: rules) {
                
                auto X = rule.lhs;
                bool isNullable = true;
                for (int k = 0; k < rule.rhs.size(); k++)
                    isNullable &= NULLABLE[rule.rhs[k]];
                if (isNullable) {
                    change |= (NULLABLE[X] != true);
                    NULLABLE[X] = true;
                }
                
                for(int i = 0; i < rule.rhs.size(); i++){
                    bool nullable = true;
                    auto Z = rule.rhs[i];
                    
                    for (int k = 0; k < i; k++) {
                        nullable &= NULLABLE[rule.rhs[k]];
                    }
                    if (nullable) 
                        change |= setUnion(FIRST[X], FIRST[Z]);

                    if(rule.rhs.size() == 1) {
                        change |= setUnion(FOLLOW[rule.rhs[0]], FOLLOW[X]);
                    }
                    for(int j = i + 1; j < rule.rhs.size(); j++){
                        // printf("X is %s and %dth Z is %s\n", X.c_str(), i, Z.c_str());
                        
                        nullable = true;
                        for (int k = i + 1; k < rule.rhs.size(); k++) {
                            nullable &= NULLABLE[rule.rhs[k]];
                        }
                        if (nullable)
                            change |= setUnion(FOLLOW[Z], FOLLOW[X]);
                        
                        nullable = true;
                        for (int k = i + 1; k <= j - 1; k++) {
                            nullable &= NULLABLE[rule.rhs[k]];
                        }
                        if (nullable)
                            change |= setUnion(FOLLOW[Z], FIRST[rule.rhs[j]]);
                    }
                } 
                
                auto s = rule.rhs[rule.rhs.size() - 1];
                if (!isTerminal(s))
                    change |= setUnion(FOLLOW[s], FOLLOW[X]);

            }
        }
        // printf("cnt: %d\n", cnt);
        for(auto s: NonTerminal){
            printf("%s : Nullable: %d First Set: ", s.c_str(), NULLABLE[s]);
            for(auto a: FIRST[s])
                printf("%s ", a.c_str());
            printf("FOLLOW Set: ");
            for(auto a: FOLLOW[s])
                printf("%s ", a.c_str());
            printf("\n");
        }
        printf("-------------------------------------------\n");
        // construct Parse Table
        for (int i = 0; i < rules.size(); i++) {
            auto rule = rules[i];
            bool fg = true;
            int idx = 0;
            while(fg){
                if(idx >= rule.rhs.size())break;
                auto u = rule.rhs[idx];
                fg = false;
                for(string a: FIRST[u]){
                    if(isTerminal(a) & a != "''") {
                        if(ParseTable[rule.lhs].find(a) != ParseTable[rule.lhs].end() && ParseTable[rule.lhs][a] != i)
                            printf("Wrong: [%s %s]: %d %d\n", rule.lhs.c_str(), a.c_str(), i, ParseTable[rule.lhs][a]);
                        ParseTable[rule.lhs][a] = i;

                    }
                    else if (a == "''"){
                        idx ++;
                        fg = true;  
                    }
                }
            }
            if (NULLABLE[rule.lhs] && rule.rhs[0] == "''")
                for(string b: FOLLOW[rule.lhs]){
                    if(!isTerminal(b) || b == "''") continue;
                    if(ParseTable[rule.lhs].find(b) != ParseTable[rule.lhs].end() && ParseTable[rule.lhs][b] != i)
                        printf("Wrong: [%s %s]: %d %d\n", rule.lhs.c_str(), b.c_str(), i, ParseTable[rule.lhs][b]);
                    ParseTable[rule.lhs][b] = i;
                    if(b == "$") {
                        ParseTable[rule.lhs]["$"] = i;
                    }
                }
                        
            
            
        }
        for(auto a: ParseTable) {
            printf("%s: \n", a.first.c_str());
            for(auto b: a.second) {
                printf("[%s %s]", a.first.c_str(), b.first.c_str());
                Rule rule = rules[b.second];
                printf(" %s ::=", rule.lhs.c_str());
                for(string u: rule.rhs) {
                    printf(" %s", u.c_str());
                }
                printf("\n");

            }
        }
        vector<string> input = readFromCode(file2);
        input.push_back("$");
        // for(auto c: input) {
        //     printf("%s\n", c.c_str());
        // }
        int nxt = 0;
        // parsing alg
        stack<string> stk;
        stk.push("S");
        int step = 0;
        while(!stk.empty()) {
            string a = stk.top();
            if(isTerminal(a)) {
                if(a == "$" && stk.top() == "S") {
                    printf("Accepted\n");
                    break;
                }
                if(a == input[nxt]){
                    if(nxt < input.size())
                        printf("Stack top: %s, begining of remaining input: %s\n", a.c_str(), input[nxt].c_str());
                    stk.pop(); 
                    step++;
                    printf("Step %d: Match %s with %s\n", step, a.c_str(), input[nxt].c_str());
                    nxt += 1;
                } else {
                    printf("Error: stack: %s and input: %s not match\n", a.c_str(), input[nxt].c_str());
                    break;
                }
            }
            else {
                string input_val = input[nxt];
                // if(input[nxt] == "ID") input_val = "id";
                // if(input[nxt] == "INTLITERAL") input_val = "intliteral";
                // if(input[nxt] == "STRINGLITERAL") input_val = "stringliteral";
                if(ParseTable[a].find(input_val) == ParseTable[a].end()){
                    printf("Error: stack: %s to input: %s no rule\n", a.c_str(), input_val.c_str());
                    break;
                } else {
                    if(nxt < input.size())
                        printf("Stack top: %s, begining of remaining input: %s\n", a.c_str(), input[nxt].c_str());
                    stk.pop();
                    Rule rule = rules[ParseTable[a][input_val]];
                    if(rule.rhs[0] == "''") {
                        step++;
                        printf("Step %d: Reduce by %s -> empty\n", step, rule.lhs.c_str());
                        continue;
                    }
                    for(int i = rule.rhs.size()-1; i >= 0; i--) {
                        stk.push(rule.rhs[i]);
                    }
                    step++;
                    printf("Step %d: Reduce by %s -> ", step, rule.lhs.c_str());
                    for(string s: rule.rhs) {
                        printf("%s ", s.c_str());
                    }
                    printf("\n");
                    }
            }
        }

    }


    return 0;
}
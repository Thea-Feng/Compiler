/**
 * --------------------------------------
 * CUHK-SZ CSC4180: Compiler Construction
 * Assignment 2: Oat v.1 Scanner
 * --------------------------------------
 * Author: Mr.Liu Yuxuan
 * Position: Teaching Assisant
 * Date: February 27th, 2024
 * Email: yuxuanliu1@link.cuhk.edu.cn
 * 
 * File: scanner.cpp
 * ------------------------------------------------------------
 * This file implements scanner function defined in scanner.hpp
 */

#include "scanner.hpp"

DFA::~DFA() {
    for (auto state : states) {
        state->transition.clear();
        delete state;
    }
}

void DFA::print() {
    printf("DFA:\n");
    for (auto state : states){
        state->print();
    }
}

/**
 * EPSILON NFA
 * (Start) -[EPSILON]-> (End)
 */
NFA::NFA() {
    start = new State();
    end = new State();
    start->transition[EPSILON] = {end};
}

/**
 * NFA for a single character
 * (Start) -[c]-> (End)
 * It acts as the unit of operations like union, concat, and kleene star
 * @param c: a single char for NFA
 * @return NFA with only one char
 */
NFA::NFA(char c) {
    start = new State();
    end = new State();
    start->transition[c] = {end};
}

NFA::~NFA() {
    for (auto state : iter_states()) {
        state->transition.clear();
        delete state;
    }
}

/**
 * Concat a string of char
 * Start from the NFA of the first char, then merge all following char NFAs
 * @param str: input string
 * @return
 */
NFA* NFA::from_string(std::string str) {
    // TODO
    NFA* _nfa = new NFA();
    auto now = _nfa->start;
    now->transition.erase(EPSILON);
    for(int i = 0; i < str.length(); i++){
        now->transition[str[i]] = {new State()};
        now = *(now->transition[str[i]].begin());
    }
    _nfa->end = now;

    return _nfa;
}

/**
 * RegExp: [a-zA-Z]
 * @return
 */
NFA* NFA::from_letter() {
    // TODO
    NFA* _nfa = new NFA();
    auto now = _nfa->start;
    now->transition.erase(EPSILON);

    for(char a = 'a'; a <= 'z'; a++){
        now->transition[a] = {_nfa->end};
        // now = *(now->transition[a].begin());
        // now->transition[EPSILON] = {_nfa->end};
    }
    for(char a = 'A'; a <= 'Z'; a++){
        now->transition[a] = {_nfa->end};
        // now = *(now->transition[a].begin());
        // now->transition[EPSILON] = {_nfa->end};
    }
    return _nfa;
}

/**
 * RegExp: [0-9]
 * @return
 */
NFA* NFA::from_digit() {
    // TODO
    NFA* _nfa = new NFA();
    auto now = _nfa->start;
    now->transition.erase(EPSILON);

    for(int a = '0'; a <= '9'; a++){
        now->transition[a] = {_nfa->end};
        // now = *(now->transition[a].begin());
        // now->transition[EPSILON] = {_nfa->end};
    }
    return _nfa;
}

/**
 * NFA for any char (ASCII 0-127)
 */
NFA* NFA::from_any_char(int except=EPSILON) {
    // TODO
    NFA* _nfa = new NFA();
    auto now = _nfa->start;
    now->transition.erase(EPSILON);
    for(int a = 0; a <= 127; a++){
        if(a == except) continue;
        now->transition[static_cast<char>(a)] = {_nfa->end};
    }
    return _nfa;
}
/**
 * Concatanat two NFAs
 * @param from: NFA pointer to be concated after the current NFA
 * @return: this -> from
 */
void NFA::concat(NFA* from) {
    // TODO
    if(this->end->transition.find(EPSILON) == this->end->transition.end())
        this->end->transition[EPSILON] = {from->start};
    else this->end->transition[EPSILON].insert(from->start);
    this->end = from->end;
}

/**
 * Set Union with another NFA
 * @param
 */
void NFA::set_union(NFA* from) {
    // TODO
   if(this->start->transition[EPSILON].size() == 1 && 
    this->start->transition[EPSILON].find(this->end) != this->start->transition[EPSILON].end()) {
        this->start->transition[EPSILON] = {from->start};
    }
    else {
        this->start->transition[EPSILON].insert(from->start);
    }
    if(from->end->transition.find(EPSILON) == from->end->transition.end())
        from->end->transition[EPSILON] = {this->end};
    else from->end->transition[EPSILON].insert(this->end);



    // State* new_st = new State();
    // new_st->transition[EPSILON] = {this->start, from->start};
    // State* new_end = new State();
    // if(this->end->transition.find(EPSILON) != this->end->transition.end())
    //     this->end->transition[EPSILON].insert(new_end);
    // else
    //     this->end->transition[EPSILON] = {new_end};
    // if(from->end->transition.find(EPSILON) != from->end->transition.end())
    //     from->end->transition[EPSILON].insert(new_end);
    // else
    //     from->end->transition[EPSILON] = {new_end};
    // this->start = new_st;
    // this->end = new_end;
}

/**
 * Set Union with a set of NFAs
 */
void NFA::set_union(std::set<NFA*> set) {
    // TODO
}

/**
 * Kleene Star Operation -> *
 */
void NFA::kleene_star() {
    // TODO
    State* new_st = new State();
    State* new_ed = new State();
    new_st->transition[EPSILON] = {this->start,new_ed};
    this->end->transition[EPSILON] = {new_ed};
    new_ed->transition[EPSILON] = {this->start};
    this->start = new_st;
    this->end = new_ed;
}

/**
 * Determinize NFA to DFA by subset construction
 * @return DFA
 */
std::vector<DFA::State*> NFA::to_DFA() {
    // TODO
    // printf("-----------to_dfa_________\n");
    // DFA* dfa = new DFA::DFA;
    std::vector<DFA::State*> states;
    std::queue<std::set<State*>> Dstate;
    std::map<std::set<State*>, DFA::State* > mark;
    states.clear();

    auto start_closure = epsilon_closure(this->start);
    Dstate.push(start_closure);
    mark[start_closure] = new DFA::State();
    states.push_back(mark[start_closure]);
    // if(start_closure.find(this->end) != start_closure.end())
    //     dfa->start
    
    while(!Dstate.empty()){
        auto T = Dstate.front();

        Dstate.pop();
        for(int a = 0; a < 128; a++){
            char c = static_cast<char>(a);
            auto _move = move(T, c);
            if(_move.size() == 0) continue;
            auto U = epsilon_closure(_move);
            if(mark.find(U) == mark.end()) {
                Dstate.push(U);
                mark[U] = new DFA::State();
                int priority = 0;
                for(auto state: U){
                    if(state->accepted && state->precedence > priority) {
                        priority = state->precedence;
                        mark[U]->accepted = true;
                        mark[U]->token_class = state->token_class;
                    }
                }
                states.push_back(mark[U]);
            }
            mark[T]->transition[c] = mark[U];
                // Dtrans[mark[T], c] = U;

        }
    }
    return states;
    

}
bool DFA::equal(State* x, State* y, char c){
   if(x->transition.find(c) == x->transition.end() && y->transition.find(c) == y->transition.end()) return true;
   if(x->transition.find(c) == x->transition.end()) return false;
   if(y->transition.find(c) == y->transition.end()) return false;
   return x->transition[c]->id != y->transition[c]->id;

}

void DFA::optimized(){
    int fg = 1;
    int cnt = 0;
    while(fg) {
        fg = 0;
        cnt++;
        for(int i = 0; i < this->states.size(); i++)
            for(int j = i + 1; j < this->states.size(); j++){
                bool equ = true;
                auto x = this->states[i], y = this->states[j];
                if(!equal(x, y, EPSILON)) continue;
                for(int a = 0; a < 128; a++){
                    char c = static_cast<char>(a);
                    if(!equal(x, y, c)) {equ = false; break;}
                }
                    
                if(equ) {
                    fg++; 
                    y->id = x->id;
                    this->states.erase(this->states.begin() + j);
                    j--;
                }
            }
        // for(auto state: this->states) printf("%d -> %d\n", ID_map[state->id], state->id);
    }
}

/**
 * Get the closure of the given Nstates set
 * It means all the Nstates can be reached with the given Nstates set without any actions
 * @param state: State* , the starting state of getting EPSILON closure
 * @return {set<State&>} The closure of state
 */ 
std::set<NFA::State*> NFA::epsilon_closure(NFA::State* state) {
    // TODO
    std::queue<State*> states_to_go{};
    states_to_go.emplace(state);
    std::set<State*> visited_states = {state};

    while(!states_to_go.empty()) {
        State* state = states_to_go.front();
        states_to_go.pop();
        for (auto neighbor : state->transition[EPSILON]) {
            if (visited_states.find(neighbor) == visited_states.end()) {
                states_to_go.emplace(neighbor);
                visited_states.insert(neighbor);
            }
        }
    }

    return visited_states;
    
}

std::set<NFA::State*> NFA::epsilon_closure(std::set<State*> states) {
    // TODO
    std::queue<State*> states_to_go;
    std::set<State*> visited_states;
    for(auto state: states){
        states_to_go.emplace(state);
        visited_states.insert(state);
    }

    while(!states_to_go.empty()) {
        State* state = states_to_go.front();
        states_to_go.pop();
        if(state->transition.find(EPSILON) != state->transition.end())
            for (auto neighbor : state->transition[EPSILON]) {
                if (visited_states.find(neighbor) == visited_states.end()) {
                    states_to_go.emplace(neighbor);
                    visited_states.insert(neighbor);
                }
            }
    }

    return visited_states;
    
}

/**
 * Get the set of neighbor states from the closure of starting state through char c
 * @param closure
 * @param c
 * @return
 */
std::set<NFA::State*> NFA::move(std::set<NFA::State*> closure, char c) {
    // TODO
    std::queue<State*> states_to_go{};
    std::set<NFA::State*> ret_closure{};
    for(auto state: closure){
        states_to_go.emplace(state);
    }
    while(!states_to_go.empty()) {
        State* state = states_to_go.front();
        states_to_go.pop();
        if(state->transition.find(c) != state->transition.end())
            for (auto neighbor : state->transition[c]) {
                if (ret_closure.find(neighbor) == ret_closure.end()) {
                    ret_closure.insert(neighbor);

                }
            }
    }
    return ret_closure;
}

void NFA::print() {
    printf("NFA:\n");
    for (auto state : iter_states())
        state->print();
}

/**
 * BFS Traversal
 */
std::vector<NFA::State*> NFA::iter_states() {
    std::vector<State*> states{};
    states.emplace_back(start);
    std::queue<State*> states_to_go{};
    states_to_go.emplace(start);
    std::set<State*> visited_states = {start};
    while(!states_to_go.empty()) {
        State* state = states_to_go.front();
        states_to_go.pop();
        for (auto trans : state->transition) {
            for (auto neighbor : trans.second) {
                if (visited_states.find(neighbor) == visited_states.end()) {
                    states_to_go.emplace(neighbor);
                    visited_states.insert(neighbor);
                    states.emplace_back(neighbor);
                }
            }
        }
    }
    return states;
}


/**
 * Constructor: Scanner
 * @usage: Scanner origin;
 *         Scanner scanner(reserved_word_strs, token_strs, reserced_word_num, token_num);
 * --------------------------------------------------------------------------------------
 * Create a Scanner object. The default constructor will not be used, and the second form
 * will create the NFA and DFA machines based on the given reserved words and tokens
 */
Scanner::Scanner() {
    nfa = new NFA();
    dfa = new DFA();
}

/**
 * Given a filename of a source program, print all the tokens of it
 * @param {string} filename
 * @return 0 for success, -1 for failure
 */ 
int Scanner::scan(std::string &filename) {
    // TODO
    auto now = dfa->states[0];
    char c;
    std::vector <char> buf;
    std::ifstream in = std::ifstream(filename);
    while(in.get(c)){
        if(now->transition.find(c) != now->transition.end()){
            if(in.eof()){
                buf.push_back(c);
                if(now->accepted){
                    std::cout << token_class_to_str(now->token_class) << " ";
                    for(auto a: buf) std::cout<<a;
                    std::cout<<"\n";
                    now = dfa->states[0];
                }
                else{
                    now = dfa->states[0];
                }
                buf.clear();
            }else {
                while(!in.eof() && now->transition.find(c) != now->transition.end()){
                    now = now->transition[c];
                    buf.push_back(c);
                    in.get(c);
                }
                in.unget();
                if(now->accepted){
                    std::cout << token_class_to_str(now->token_class) << " ";
                    for(auto a: buf) std::cout<<a;
                    std::cout<<"\n";
                    now = dfa->states[0];
                }
                else{
                    now = dfa->states[0];
                }
                buf.clear();
            }
            
        }
        else 
            continue;
    }

    return 0;
}

/**
 * Add string tokens, usually for reserved words, punctuations, and operators
 * @param token_str: exact string to match for token recognition
 * @param token_class
 * @param precedence: precedence of token, especially for operators
 * @return
 */
void Scanner::add_token(std::string token_str, TokenClass token_class, unsigned int precedence) {
    auto keyword_nfa = NFA::from_string(token_str);
    keyword_nfa->set_token_class_for_end_state(token_class, precedence);
    nfa->set_union(keyword_nfa);
    // std::cout<<token_str<<" token finished"<<"\n";

}

/**
 * Token: ID (Identifier)
 * RegExp: [a-zA-Z][a-zA-Z0-9_]*
 * @param token_class
 * @param precedence
 * @return
 */
void Scanner::add_identifier_token(TokenClass token_class, unsigned int precedence) {
    // TODO: mimic how add_token do

    auto identifier_nfa = NFA::from_letter();
    auto letter_digit_nfa = NFA::from_letter();
    letter_digit_nfa->set_union(NFA::from_digit());
    letter_digit_nfa->set_union(new NFA('_'));
    letter_digit_nfa->kleene_star();
    identifier_nfa->concat(letter_digit_nfa);
    identifier_nfa->set_token_class_for_end_state(token_class, precedence);
    nfa->set_union(identifier_nfa);
    // printf("ID added\n");
}

/**
 * Token: INTEGER
 * RegExp: [0-9]+
 * Negative integer is recognized by unary operator MINUS
 * @param token_class
 * @param precedence
 * @return
 */
void Scanner::add_integer_token(TokenClass token_class, unsigned int precedence) {
    // TODO: mimic how add_token do
    auto integer_nfa = NFA::from_digit();
    // integer_nfa->print();
    // printf("------------------------\n");
    auto more_integer_nfa = NFA::from_digit();
    more_integer_nfa->kleene_star();
    // more_integer_nfa->print();
    // printf("------------------------\n");

    integer_nfa->concat(more_integer_nfa);
    // integer_nfa->print();
    // printf("------------------------\n");
    integer_nfa->set_token_class_for_end_state(token_class, precedence);
    nfa->set_union(integer_nfa);
    // printf("Integer added\n");
}

/**
 * Token Class: STRINGLITERAL
 * RegExp: "(.)*"
 * @param token_class
 * @param precedence
 * @return
 */
void Scanner::add_string_token(TokenClass token_class, unsigned int precedence) {
    // TODO: mimic how add_token do
    auto string_nfa = new NFA('"');
    auto content_nfa = NFA::from_any_char(34);
    content_nfa->kleene_star();
    string_nfa->concat(content_nfa);
    string_nfa->concat(new NFA('"'));
    string_nfa->set_token_class_for_end_state(token_class, precedence);
    nfa->set_union(string_nfa);
}

/**
 * Token Class: COMMENT
 * RegExp: \/\*(.)*\*\/
 * @param token_class
 * @param precedence
 * @return
 */
void Scanner::add_comment_token(TokenClass token_class, unsigned int precedence) {
    // TODO: mimic how add_token do
    auto comment_nfa = new NFA('/');
    comment_nfa->concat(new NFA('*'));
    auto content_nfa = NFA::from_any_char(42);
    content_nfa->kleene_star();
    comment_nfa->concat(content_nfa);
    comment_nfa->concat(new NFA('*'));
    comment_nfa->concat(new NFA('/'));
    comment_nfa->set_token_class_for_end_state(token_class, precedence);
    nfa->set_union(comment_nfa);
}

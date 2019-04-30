#include <iostream>
#include <unistd.h>
#include <chrono>
#include <ctime>
// A simple class with a constuctor and some methods...
class Foo
{
    public:
        Foo(int);
        void bar();
        int foobar(int);

        void thread1();
        void thread2();
    private:
        int val;
        std::chrono::_V2::system_clock::time_point start;
};

Foo::Foo(int n)
{
    val = n;
    std::chrono::_V2::system_clock::time_point start = std::chrono::system_clock::now();
}

void Foo::bar()
{
    std::cout << "Value is " << val << std::endl;
}

int Foo::foobar(int n)
{
    return val + n;
}

void Foo::thread2()
{
    usleep(1000*200); //
    std::chrono::_V2::system_clock::time_point end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end-start;
    std::time_t end_time = std::chrono::system_clock::to_time_t(end);

    std::cout << "t2 ******** " << std::ctime(&end_time);
              // << "elapsed time: " << elapsed_seconds.count() << "s\n";

}

void Foo::thread1()
{
    std::cout << "CALL INTO THREAD 1 ************************";
    usleep(1000*1000*10);
    std::chrono::_V2::system_clock::time_point end = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = end-start;
    std::time_t end_time = std::chrono::system_clock::to_time_t(end);

    std::cout << "CALL OUT OF THREAD 1 : ********** " << std::ctime(&end_time);
              // << "elapsed time: " << elapsed_seconds.count() << "s\n";

}
// #error nice


// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
    Foo* Foo_new(int n) {return new Foo(n);}
    void Foo_bar(Foo* foo) {foo->bar();}
    int Foo_foobar(Foo* foo, int n) {return foo->foobar(n);}
    void Foo_thread1(Foo* foo) {foo->thread1();}
    void Foo_thread2(Foo* foo) {foo->thread2();}
}

/* From http://www.auctoris.co.uk/2017/04/29/calling-c-classes-from-python-with-ctypes/
 *
 * Compile with
 * g++ -c -fPIC threadTest.cpp -o threadTest.o && g++ -shared -W -o threadTest.so threadTest.o
 */
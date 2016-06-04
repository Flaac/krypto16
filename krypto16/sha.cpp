#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <string>
#include <vector>
#include <bitset>
#include <stdlib.h>
#include <math.h>

using namespace std;

unsigned long int K[64] = {
   0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

const string padding = "00000000";

unsigned int ch(unsigned int x, unsigned int y, unsigned int z)
{
    return (x & y) ^ ((~x) & z);
}

unsigned int maj(unsigned int x, unsigned int y, unsigned int z)
{
    return (x & y) ^ (x & z) ^ (y & z);
}

unsigned int rightrotate(unsigned int x, int n)
{
    return (x << (32-n)) | (x >> n);
}

unsigned int rightshift(unsigned int x, int n)
{
    return x >> n;
}

unsigned int sum0(unsigned int x)
{
    return rightrotate(x,2) ^ rightrotate(x,13) ^ rightrotate(x,22);
}

unsigned int sum1(unsigned int x)
{
    return rightrotate(x,6) ^ rightrotate(x,11) ^ rightrotate(x,25);
}

unsigned int sig0(unsigned int x)
{
    return rightrotate(x,7) ^ rightrotate(x,18) ^ rightshift(x,3);
}

unsigned int sig1(unsigned int x)
{
    return rightrotate(x,17) ^ rightrotate(x,19) ^ rightshift(x,10);
}


int main()
{
//    ifstream fichier("sample.in");
//    if(fichier)
//    {

        string t;
        while(getline(cin, t))
        {
            ///Padding - Adding a 1-bit at the end of the message
            long long int oldSize = t.size();
            t = t + "80";
            int l = t.size() % 8;
            if(l!=0)
            {
                t = t + padding.substr(0,8-l);
            }


            ///Casting the data into a vector of unsigned int*
            vector<unsigned int* > chunk;
            int j = 0;
            bool endstring = false;
            while(!endstring)
            {
                string temp = "";
                if(t.size()>128*(j+1))
                {
                    temp = t.substr(j*128,128);
                }
                else
                {
                    if(t.size() > 128*(j))
                    {
                        temp = t.substr(j*128,t.size() - j*128);
                    }
                    else
                    {
                        endstring = true;
                    }
                }
                j = j + 1;
                if(!endstring)
                {
                    unsigned int* listnum = new unsigned int[16];
                    for(int i=0;i<16;++i)
                    {
                        string test = "";
                        if(temp.size() >= (i+1)*8)
                        {
                            test = temp.substr(i*8,8);
                        }
                        else
                        {
                            if(temp.size() >= 8*i)
                            {
                                test = temp.substr(i*8,temp.size() - 8*i);
                            }
                        }
                        const char* tempc = test.c_str();
                        listnum[i] = (int)strtol(tempc, NULL, 16);
                    }
                    chunk.push_back(listnum);
                }
            }

            ///Padding - Adding the length of the message at the end
            unsigned long int lengthm = (oldSize * 4);
            unsigned int leftpart = lengthm >> 32;
            unsigned int rightpart = (lengthm << 32) >> 32;
            if(chunk[chunk.size()-1][15] != 0 || chunk[chunk.size()-1][14] != 0)
            {
                unsigned int* listnum = new unsigned int[16];
                for(int i=0;i<16;++i)
                {
                    listnum[i] = 0;
                }
                chunk.push_back(listnum);
            }
            long long int last = chunk.size() - 1;
            chunk[last][14] = leftpart;
            chunk[last][15] = rightpart;



            ///Initialisation
            int Rounds = 64;
            long long int lengthChunk = chunk.size();
            unsigned long int** H = new unsigned long int*[lengthChunk + 1];
            for(long long int k = 0;k<lengthChunk+1;++k)
            {
                H[k] = new unsigned long int[8];
                for (int m = 0;m<8;++m)
                {
                    H[k][m] = 0;
                }
            }

            H[0][0] = 0x6a09e667;
            H[0][1] = 0xbb67ae85;
            H[0][2] = 0x3c6ef372;
            H[0][3] = 0xa54ff53a;
            H[0][4] = 0x510e527f;
            H[0][5] = 0x9b05688c;
            H[0][6] = 0x1f83d9ab;
            H[0][7] = 0x5be0cd19;

            unsigned long int a = H[0][0];
            unsigned long int b = H[0][1];
            unsigned long int c = H[0][2];
            unsigned long int d = H[0][3];
            unsigned long int e = H[0][4];
            unsigned long int f = H[0][5];
            unsigned long int g = H[0][6];
            unsigned long int h = H[0][7];

            ///Main loop
            for(int i=1;i<lengthChunk+1;++i)
            {
                a = H[i-1][0];
                b = H[i-1][1];
                c = H[i-1][2];
                d = H[i-1][3];
                e = H[i-1][4];
                f = H[i-1][5];
                g = H[i-1][6];
                h = H[i-1][7];
                for(int j=0;j<Rounds;++j)
                {
                    ///Compute W
                    unsigned long int* W = new unsigned long int[64];
                    for (int s=0;s<16;++s)
                    {
                        W[s] = (unsigned long int) chunk[i-1][s];
                    }
                    for(int s=16;s<64;++s)
                    {
                        W[s] = ((unsigned long int) sig1(W[s-2])) + W[s-7] + ((unsigned long int)sig0(W[s-15])) + W[s-16];
                    }

                    ///Main computation
                    unsigned long int t1 = h + ((unsigned long int)sum1(e)) + ((unsigned long int)ch(e,f,g)) + K[j] + W[j];
                    unsigned long int t2 = ((unsigned long int)sum0(a)) + ((unsigned long int)maj(a,b,c));
                    h = g;
                    g = f;
                    f = e;
                    e = d + t1;
                    d = c;
                    c = b;
                    b = a;
                    a = t1 + t2;
                }
                H[i][0] = a + H[i-1][0];
                H[i][1] = b + H[i-1][1];
                H[i][2] = c + H[i-1][2];
                H[i][3] = d + H[i-1][3];
                H[i][4] = e + H[i-1][4];
                H[i][5] = f + H[i-1][5];
                H[i][6] = g + H[i-1][6];
                H[i][7] = h + H[i-1][7];
            }

            ///Print final result
            for(int j=0;j<8;++j)
            {
                printf( "%08.8x", (unsigned int) H[lengthChunk][j]);
            }
            cout << endl;
        }
    return 0;
}


#include <bits/stdc++.h>
#define ll long long
using namespace std;

ll N;
int K;
ll divnum = 1000000007;

int main() {
  cin >> N >> K;
  ll count=0;
  ll *num;

  ll now=1, next;
  vector<int> lens;
  while (now<=N) {
    next = N/(N/now);
    lens.push_back(next-now+1);
    now = next+1;
  }
  ll len_size = lens.size();
  num = new ll[2*len_size];

  ll offset, preoffset=0;z
  ll tmp;
  for(int s=0; s<len_size; s++) {
    num[s] = 1;
  }
  for(int k=1; k<K; k++) {
    offset = (k % 2) * len_size;
    tmp = 0;
    for(int s=0; s<len_size; s++) {
      tmp = (tmp + num[preoffset+s]*lens[s]) % divnum;
      num[offset+len_size-1-s] = tmp;
    }
    preoffset = offset;
  }

  ll res=0;
  offset = ((K-1) % 2) * len_size;
  for (int s=0; s<len_size; s++) {
    res = (res + num[offset+s]*lens[s]) % divnum;
  }
  cout << res << endl;
}

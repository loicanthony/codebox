/*------------------------------------------------------------*/
/*  File        : bb.cpp                                      */
/*  Author      : Christophe Tribes                           */
/*  Date        : 2017-08                                     */
/*  Description : Spring problem                              */
/*                n=3                                         */
/*                m=4                                         */
/*------------------------------------------------------------*/
#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

#define dim 3

/*-----------------------------------*/
/*           main function           */
/*-----------------------------------*/
int main ( int argc, char ** argv ) {

  // input read :
  // ------------
  double z = 1e+20;
  if ( argc < 2 )
  {
    cout << z << endl;
    return 1;
  }
  ifstream in ( argv[1] );
  if ( in.fail() ) {
    cout << z << endl;
    return 1;
  }

    double D,d,N;
  // read :
 in >> D >> d >> N ;

  if ( in.fail() ) {
    cout << z << endl;
    return 1;
  }
  in.close();

  // black-box eval :
  // ----------------
    double fout = 10.0*(N+2.0)*D*d*d;
    
    double c1 = -N*pow(D,3.0)/71875.0/pow(d,4.0)+1.0;
    double c2 = -1.0+1.0/5108.0/d/d + ( 4.0*D*D -d*D )/12566.0/(D*pow(d,3.0) - pow(d,4.0));
    double c3 = -140.45 * d/D/D/N + 1.0;
    double c4 = -1.0 + (D+d)/1.5 ;

    cout << fout << " " << c1 <<" " << c2 << " " << c3 << " " << c4 << endl;

  return 0;
}

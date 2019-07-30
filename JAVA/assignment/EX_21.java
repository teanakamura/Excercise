// EX_21.java
// 19M31252 仲村 風哉
package assignment;

public class EX_21 {
	public static void main(String[] args) {
		MyPoint myPoint = new MyPoint(10, 20); myPoint.print();
		MyPoint myPoint2 = new MyPoint(30); myPoint2.print();
	}
}

class MyPoint {
	int x, y;
	public MyPoint(int wx, int wy) {
		x=wx; y=wy;
	}
	public MyPoint(int wy) {
		x=0; y=wy;
	}
	public void print() {
		System.out.println("(" + x + ", " + y + ")");
	}
}
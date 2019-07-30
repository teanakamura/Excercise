// EX_4.java
// 19M31252 仲村 風哉
package assignment;

public class EX_4 {
	public static void main(String[] args) {
		int dividend = 100;
		int start = -10;
		int end = 11;
		divOut(dividend, start, end);
	}
	
	final private static void divOut(int dividend, int start, int end) {
		for (int i = start; i < end; i++) {
			try {
				System.out.println(dividend / i);
			} catch (ArithmeticException ex) {  // exceptionが発生するのはint/0の場合のみ。
				// System.out.println(ex);
				System.out.println("zero division error.");
			}
		}
	}
}
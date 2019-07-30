// EX_6.java
// 19M31252 仲村 風哉
package assignment;

public class EX_6{
	public static void main(String[] args) {
		for (int i = 0; i < 10; ++i) {
			// new SubThread1().start();
			new SubThread1(i).start();
		}
	}
}
class SubThread1 extends Thread {
	String num = "None";
	
	public SubThread1() {
		super();
	}
	
	public SubThread1(int i) {
		num = "No." + String.valueOf(i);
	}
	
	@Override
	public void run() {
		String out = "サブスレッド" +
				(num != "None" ? num : "") +
				"からの出力";
		System.out.println(out);
	}
}
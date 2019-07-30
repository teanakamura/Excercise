// EX_22.java
// 19M31252 仲村 風哉
package assignment;

public class EX_22 {
	public static void main(String[] args) {
		MyObj1 myObj1 = new MyObj1();
		myObj1.value = 100;
		myObj1.value = 50;
		System.out.println(myObj1.value);
		MyObj2 myObj2 = new MyObj2();
		myObj2.setValue(80);
		System.out.println(myObj2.getValue());
		System.out.println(myObj2.doubleValue());
	}
}

// データ隠蔽していないクラス
class MyObj1 {
    int value;
}

// データ隠蔽しているクラス
class MyObj2 {
	private int value;
	public void setValue(int v) {
		value = v;
	}
	public int getValue() {
		return value;
	}
	public int doubleValue() {
		return value*2;
	}
}
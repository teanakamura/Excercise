// EX_11.java
// 19M31252 仲村 風哉
package assignment;

public class EX_11 {
	public static void main(String[] args) {
		int N = Integer.parseInt(args[0]);
		// 配列変数の定義
		int[] trib;
		trib = new int[N];
		
		// 配列への値の代入
		trib[0] = 1; trib[1] = 1; trib[2] = 2;
		for (int i = 3; i < N; ++i) {
			trib[i] = trib[i-1] + trib[i-2] + trib[i-3];
		}
		System.out.println("トリボナッチ数列");
		for (int i = 0; i < trib.length; ++i) {
			System.out.println( trib[i] );
		}
	}
}
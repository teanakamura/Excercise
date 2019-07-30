// EX_12.java
// 19M31252 仲村 風哉
package assignment;

public class EX_12 {
	public static void main(String[] args) {
		float[][] mat = {
			{1, 1, 2},
			{2, 4, 6},
			{3, 5, 7}
		};
		System.out.println(determinant_dim3(mat));;
	}
	
	private static float determinant_dim3(float[][] mat) {
		float det = 0;
		float add, sub;
		for (int i=0; i<3; i++) {
			add = mat[0][i%3] * mat[1][(i+1)%3] * mat[2][(i+2)%3];
			sub = mat[0][(i+2)%3] * mat[1][(i+1)%3] * mat[2][i%3];
			det += (add - sub);
		}
		return det;
	}
}

// EX_ac.java
// 19M31252 仲村 風哉
package assignment;

interface Cool {
	public void cool();
}

interface Ventilation {
	public void ventilation();
}

public class EX_ac {
	public static void main(String[] args) {
		AirConditioner ac = new AirConditioner("24");
		ac.cool();
		ac.ventilation();
		ac.cool();
	}
}

class Cooler implements Cool {
	public String setPoint;
	public Cooler(String p) {
		setPoint = p;
	}
	public void cool() {
		System.out.println(setPoint);
	}
}

class AirConditioner extends Cooler implements Ventilation {
	public int best = 22;
	public AirConditioner(String p) {
		super(p);
	}
	public void ventilation() {
		float temp = Float.parseFloat(setPoint);
		if (temp > best+1) {
			temp -= 1;
		} else if (temp < best-1) {
			temp += 1;
		} else {
			temp = best;
		}
		setPoint = (int)temp == temp ? String.valueOf((int)temp) : String.valueOf(temp);
	}
}
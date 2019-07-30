// EX_5.java
// 19M31252 仲村 風哉
package assignment;

import java.util.List;
import java.util.ArrayList;
import java.time.Month;
import java.time.format.TextStyle;
import java.util.Locale;

public class EX_5 {
	public static void main(String[] args) {
		List<String> monthNames = getMonthNames();
		monthNames.stream()
			.filter(m -> m.contains("e"))
			.forEach(m -> System.out.println(m));
	}
	
	final private static List<String> getMonthNames() {
		List<String> ret = new ArrayList<>();
		for (int i=1; i <= 12; i++) {
			ret.add(Month.of(i).getDisplayName(TextStyle.FULL,Locale.ENGLISH));
		}
		return ret;
	}
}
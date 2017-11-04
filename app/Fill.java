public class Fill {

	public static void print_mat(int[][] mat) {
		String retVal = ""
		for(int i = 0; i < mat.length; i++) {
			for(int j = 0; j < mat[0].length; j++) {
				retVal += mat[i][j];
			}
			retVal += "\n";
		}
		System.out.println(retVal);
	}

	public static void fill_mat(int rows, int cols) {
		int[][] mat = new int[rows][cols]
		for(int i = 0; i < rows; i++) {
			for(int j = 0; j < cols; j++) {
				mat[i][j] = i + j;
			}
		}
		print_mat(mat);
	}

	public static void main(String[] args) {

	}

}
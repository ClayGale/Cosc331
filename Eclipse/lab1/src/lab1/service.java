package lab1;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class service {
	
	private static String readCSS(){		
		BufferedReader read;
		try {
			read = new BufferedReader(new FileReader("src/lab1/template.css"));

			String line;
			String output = "";

			while((line = read.readLine()) != null) {
				line = line.replaceAll("\n", "");
				output = output + line.replaceAll("\t", "");

			}
			read.close();
			return output;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	private static String substituteCSS(String css, String accentC, String mainC, String font) {

		css = css.replaceAll("_MAIN_COLOUR_", "#" + mainC);
		css = css.replaceAll("_ACCENT_COLOUR_", "#" + accentC);
		css = css.replaceAll("_FONT_FAMILY_", "#" + font);
		
		return css;
	}
	
	private static String verifyHex(String rawInput, String defaultValue) {

		try {
			Long.parseLong(rawInput,16);
			if(rawInput.length() <= 6) {
				return rawInput;
			}
			else {
				return defaultValue;
			}
		}

		catch(Exception e) {
			e.printStackTrace();
			return defaultValue;
		}
	}

	
	private static String verifyFont(String fontInput, String defaultValue) {

		fontInput = fontInput.toLowerCase();
		if (fontInput != "serif" && fontInput != "sans-serif" && fontInput != "monospace") {
			return defaultValue;
		}
		else {
			return fontInput;
		}
	}
	
	public static void webServe(int port) throws IOException {

		ServerSocket server = new ServerSocket(port);
		while(true) {

			Socket userConn = server.accept();

			BufferedReader br = new BufferedReader(new InputStreamReader(userConn.getInputStream()), 1);
			String output = "";
			String line;

			while ((line = br.readLine()) != null) {
	            output = output + line;
	            if (line.isEmpty()) {
	                break;
	            }
	        }

			System.out.println(output);
			String mainCSS = parseHeader("main", output);
			String accentCSS = parseHeader("accent", output);
			String fontCSS = parseHeader("font", output);
			
			mainCSS = verifyHex(mainCSS, "FFFFFF");
			accentCSS = verifyHex(accentCSS, "FFFFFF");
			fontCSS = verifyFont(fontCSS, "monospace");
			
			String template = readCSS();
			String css = substituteCSS(template, accentCSS, mainCSS, fontCSS);
			String response = "HTTP/1.1 200 OK\r\n\r\n" + css;
			
			userConn.getOutputStream().write(response.getBytes("UTF-8"));
			userConn.getOutputStream().flush();

			userConn.close();
			br.close();
		}
	}
	
	public static String parseHeader(String variable, String rawInput) {
		
		String pattern = "GET /.*" + variable + "=(.*?)(?:&| HTTP)";
		Pattern regex = Pattern.compile(pattern);
		Matcher match = regex.matcher(rawInput);
		
		if(match.find()) {
			return match.group(1);
		}
		else {
			return null;
		}
		
	}
	
	public static void main(String[] args) throws IOException {
		// Begins the webserver on the specified port (Port 80 by default)
		webServe(80);
	}
	
}
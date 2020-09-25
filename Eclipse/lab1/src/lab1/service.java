package lab1;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
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
			read = new BufferedReader(new FileReader("template.css"));

			String line;
			String output = "";

			while((line = read.readLine()) != null) {
				line = line.replaceAll("\n", "");
				output = output + line.replaceAll("\t", "");

			}
			read.close();
			return output;
		} catch (IOException e) {
			// TODO Auto-generated catch block
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
		// TODO: You'll need most of your functions to run in the server loop here
		// To get you started, this code will fetch input, print it to the console
		// and then return a message to the user
		ServerSocket server = new ServerSocket(port);
		while(true) {
			// server.accept() is blocking, so your code will stop here until a connection is made
			Socket userConn = server.accept();
			// Buffered Reader for handling the input stream from the user/client
			BufferedReader br = new BufferedReader(new InputStreamReader(userConn.getInputStream()), 1);
			String output = "";
			String line;
			// Read from the buffer until the buffer is empty or the connection closes
			while ((line = br.readLine()) != null) {
	            output = output + line;
	            if (line.isEmpty()) {
	                break;
	            }
	        }
			// Print out the input from the user/client
			System.out.println(output);
			String mainCSS = parseHeader("main", output);
			String accentCSS = parseHeader("accent", output);
			String fontCSS = parseHeader("font", output);
			mainCSS = verifyHex(mainCSS);
			// Writing our response message - note that the headers must end in \r\n\r\n
			// The message itself should come after the headers, and should end in \r\n
			String helloWorld = "Hello World, This is my response message!\r\n";
			String response = "HTTP/1.1 200 OK\r\n\r\n" + helloWorld;
			// Write the HTTP message out to the output stream, back to the client/user
			userConn.getOutputStream().write(response.getBytes("UTF-8"));
			userConn.getOutputStream().flush();
			// Flush to make sure the data is sent, and then close the connection and the buffered reader
			userConn.close();
			br.close();
		}
	}
	
	public static String parseHeader(String variable, String rawInput) {
		// TODO: Write the basic parser needed to fetch our a parameter (variable)
		// from the client/user rawInput, and then return it
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
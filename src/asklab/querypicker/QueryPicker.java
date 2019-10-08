package asklab.querypicker;

import javax.swing.*;
import javax.swing.text.DefaultCaret;
import javax.swing.border.Border;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

import java.io.*;
import java.util.List;
import java.util.Arrays;
import java.util.Random;
import java.util.Vector;

import java.nio.file.*;
import java.io.File;
import java.util.*;
import java.io.FilenameFilter;

import java.awt.event.*;

//import javax.imageio.*;
/*import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.net.*;
import javax.imageio.ImageIO;
import javax.swing.event.*;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
*/

import asklab.cpsf.CPSReasoner;

class GUIHelper {
	static void setJPanelBorder(JPanel pan, String title) {
		Border bGreyLine, bTitled1, bTitled2;
		bGreyLine = BorderFactory.createLineBorder(Color.LIGHT_GRAY, 1, true);
		bTitled1 = BorderFactory.createTitledBorder(bGreyLine, title, TitledBorder.LEFT, TitledBorder.TOP);
		pan.setBorder(bTitled1);
	}

	static JPanel makeBorder(JComponent obj, String title) {
		JPanel pan = new JPanel();
		pan.setLayout(new BoxLayout(pan, BoxLayout.X_AXIS));
		pan.add(obj);
		GUIHelper.setJPanelBorder(pan, title);

		return (pan);
	}
}

class ReadStream implements Runnable {
	String name;
	InputStream is;
	Vector<String> v;
	boolean discard;
	Thread thread;

	public ReadStream(String name, InputStream is, Vector<String> v, boolean discard) {
		this.name = name;
		this.is = is;
		this.v = v;
		this.discard = discard;
	}

	public void start() {
		thread = new Thread(this);
		thread.start();
	}

	public void run() {
		try {
			InputStreamReader isr = new InputStreamReader(is);
			BufferedReader br = new BufferedReader(isr);
			while (true) {
				String s = br.readLine();
				if (s == null)
					break;
				// System.out.println ("[" + name + "] " + s);
				if (!discard)
					v.addElement(s);
			}
			is.close();
		} catch (Exception ex) {
			System.out.println("Problem reading stream " + name + "... :" + ex);
			ex.printStackTrace();
		}
	}
}

class QExecActionListener implements ActionListener {
//	public static String[] solverStrings = { "dlv", "dlv (all models)", "clingo", "clingo (all models)" };
//	private int[] solverConst = { CPSReasoner.SLVR_DLV, CPSReasoner.SLVR_DLV_ALL, CPSReasoner.SLVR_CLINGO, CPSReasoner.SLVR_CLINGO_ALL };

	private String baseDir;
	private String exDir;
	private String aspFile;
	private String tmpDir;
	private String ontologyDir;
	private String sparqlFile;
	private JTextArea taASP, taRes;
	private JProgressBar progr;
	private int solver;
	private Task task;

	class Task extends SwingWorker<Void, Void> {
		@Override
		public Void doInBackground() {
			//System.out.println("Do it here");
			try {

				tmpDir = "./tmpDir";

				try {
					deleteDirectoryStream(new File(tmpDir).toPath());
				} catch (Exception x) {
				}

				if (!new File(tmpDir).mkdir()) {
					System.err.println("unable to create the directory " + tmpDir);
					return null;
				}
				copyOWL(baseDir, tmpDir);
				copyOWL(exDir, tmpDir);
				String f = exDir + "/" + aspFile;
				Path source = new File(f).toPath();
				Path newdir = new File(tmpDir).toPath();
				try {
					Files.copy(source, newdir.resolve(source.getFileName()));
				} catch (FileAlreadyExistsException x) {
				} catch (IOException x) {
					System.err.println("Unable to copy " + f + " to " + tmpDir);
				}

				String sparqlQ = Utils.readFile(sparqlFile);
				System.out.println(sparqlFile + " loaded.");

				String aspQ = Utils.readFile(tmpDir + "/" + aspFile);

				progr.setIndeterminate(true);

				taRes.setText("");

				String res = CPSReasoner.query(sparqlQ, aspQ, tmpDir, solver);

				taRes.setText(res);

				progr.setIndeterminate(false);
			} catch (FileNotFoundException fnx) {
				JOptionPane.showMessageDialog(null, "Unable to read SPARQL query from file 'dump.sparql'", "Error",
						JOptionPane.ERROR_MESSAGE);
			} catch (IOException iox) {
				JOptionPane.showMessageDialog(null, "Unable to read SPARQL query from file 'dump.sparql'", "Error",
						JOptionPane.ERROR_MESSAGE);
			}

			return null;
		}

		public void done() {
		}
	}

	void deleteDirectoryStream(Path path) throws IOException {
		Files.walk(path).sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(File::delete);
	}

	void copyOWL(String dir, String tmpDir) {
		class OWLFilter implements FilenameFilter {
			public boolean accept(File dir, String f) {
				return (f.endsWith(".owl"));
			}
		}

		ArrayList<File> filesToCopy = new ArrayList<File>();
		File sourceDirectory = new File(dir);
		String[] toCopy = sourceDirectory.list(new OWLFilter());
		for (String file : toCopy) {
			try {
				Path source = new File(dir + "/" + file).toPath();
				Path newdir = new File(tmpDir).toPath();
				Files.copy(source, newdir.resolve(source.getFileName()));
			} catch (FileAlreadyExistsException x) {
			} catch (IOException x) {
				System.err.println("Unable to copy " + file + " to " + tmpDir);
			}
		}
	}

	public QExecActionListener(String sparqlFile, String baseDir, String exDir, String aspFile, JProgressBar progr,
			int solver, JTextArea taRes) {
		this.sparqlFile = sparqlFile;
		this.baseDir = baseDir;
		this.exDir = exDir;
		this.aspFile = aspFile;
		this.progr = progr;
		this.solver = solver;
		this.taRes = taRes;
	}

	public void actionPerformed(ActionEvent e) {
		task = new Task();
//        	task.addPropertyChangeListener(this);
		task.execute();
	}
}

class Utils {
	static String readFile(String s) throws FileNotFoundException, IOException {
		BufferedReader br = new BufferedReader(new FileReader(s));
		String res = readFile(br);
		br.close();
		return (res);
	}

	static String readFile(File f) throws FileNotFoundException, IOException {
		BufferedReader br = new BufferedReader(new FileReader(f));
		String res = readFile(br);
		br.close();
		return (res);
	}

	static String readFile(BufferedReader br) throws IOException {
		String str = "", line;
		while ((line = br.readLine()) != null)
			str = str + line + "\n";
		return (str);
	}
}

public class QueryPicker {
	public static String[] solverStrings = { "dlv", "dlv (all models)", "clingo", "clingo (all models)" };
	private int[] solverConst = { CPSReasoner.SLVR_DLV, CPSReasoner.SLVR_DLV_ALL, CPSReasoner.SLVR_CLINGO,
			CPSReasoner.SLVR_CLINGO_ALL };

	final String sparqlFile = pkgPath("dump.sparql");
	final String dataDir = pkgPath("QUERIES/");
	final String contentFile = dataDir + "content.txt";

	public static void main(String[] args) {
		new QueryPicker();
	}

	String pkgPath(String p) {
		if (getClass().getResource(p) == null) {
			System.out.println("ERROR: path does not exist: " + p);
			return ("");
		}

		return (getClass().getResource(p).getPath());
	}

	public JButton createQueryButton(String l, String sparqlFile, String baseDir, String exDir, String aspFile,
			JProgressBar progressBar, int solver, JTextArea taRes) {
		//System.out.println("\n" + l + "--" + sparqlFile + "--" + baseDir + "--" + exDir + "--" + aspFile);
		JButton btn = new JButton(l);
		btn.addActionListener(new QExecActionListener(sparqlFile, baseDir, exDir, aspFile, progressBar, solver, taRes));
		return (btn);
	}

	public void loadContent(JPanel taQs, JProgressBar progressBar, JTextArea taRes)
			throws FileNotFoundException, IOException {
		//System.out.println("---ThanhNH : " + contentFile);
		String[] content = Utils.readFile(contentFile).split("\\r?\\n");
		for (int l = 0; l < content.length; l++) {
			String line = content[l];

			// remove comments and trim spaces
			line = line.replaceFirst("%.*$", "").trim();
			if (line.equals(""))
				continue;

			// match tag
			if (line.toUpperCase().equals("*LBL")) {
				if (content.length - l <= 1)
					throw (new IOException("Unexpected end of *LBL tag in file " + contentFile));
				String lbl = content[++l];
				if (lbl.equals(""))
					/* Java will not create a label if the string is 0-length */
					lbl = " ";

				taQs.add(new JLabel(lbl));
			} else if (line.toUpperCase().equals("*QUERY")) {
				if (content.length - l <= 3)
					throw (new IOException("Unexpected end of *QUERY tag in file " + contentFile));
				String title = content[++l];
				String subdir = content[++l];
				String solverName = content[++l];
				String aspfile = content[++l];

				int solverIndex = -1;
				for (String s : solverStrings) {
					if (s.equals(solverName)) {
						solverIndex++; // compensate for starting at -1
						break;
					}
					solverIndex++;
				}
				if (solverIndex == -1) {
					solverIndex = 0;
					System.out.println("***WARNING: invalid solver name " + solverName + " in " + contentFile
							+ ". Defaulting to " + solverStrings[solverIndex]);
				}

				taQs.add(createQueryButton(title, sparqlFile, dataDir + "/BASE", dataDir + subdir, aspfile, progressBar,
						solverConst[solverIndex], taRes));
			} else
				throw (new IOException("Unexpected tag \"" + line + "\"+in file " + contentFile));
		}
	}

	public QueryPicker() {
		JFrame guiFrame = new JFrame();

		// make sure the program exits when the frame closes
		guiFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		guiFrame.setTitle("Query Picker v3 [CPSReasoner " + CPSReasoner.version() + "]");
		guiFrame.setSize(1200, 800);

		// This will center the JFrame in the middle of the screen
		guiFrame.setLocationRelativeTo(null);

		JPanel rightpan = new JPanel();
		rightpan.setLayout(new BoxLayout(rightpan, BoxLayout.Y_AXIS));
		// guiFrame.add(rightpan,BorderLayout.CENTER);

		// guiFrame.add(rightpan,BorderLayout.CENTER);

		JProgressBar progressBar = new JProgressBar(0, 100);
		progressBar.setIndeterminate(false);
		// Call setStringPainted now so that the progress bar height
		// stays the same whether or not the string is shown.
		progressBar.setString(" ");
		progressBar.setStringPainted(true);
		Border bGreyLine = BorderFactory.createLineBorder(Color.LIGHT_GRAY, 1, true);
		progressBar.setBorder(bGreyLine);
		// progressBar.setBackground (new Color (0, 0, 0, 0));
		// JComboBox solverL = new JComboBox(solverStrings);
		// solverL.setSelectedIndex(1); // dlv (all models)
		JButton runB = new JButton("Run query");
//		//runB.setEnabled(false);
//		runB.addActionListener(new ExecActionListener(tmpFile,ontologyDir,sparqlFile,taASP,taRes,progressBar,solverL));

		JTextArea taRes = new JTextArea();
		taRes.setEditable(false);
		taRes.setFont(new Font("monospaced", Font.PLAIN, 12));
		((DefaultCaret) taRes.getCaret()).setUpdatePolicy(DefaultCaret.NEVER_UPDATE);
		JScrollPane spRes = new JScrollPane(taRes);

		JPanel taQs = new JPanel();
		taQs.setLayout(new BoxLayout(taQs, BoxLayout.PAGE_AXIS));
		taQs.add(Box.createHorizontalGlue());
		try {
			loadContent(taQs, progressBar, taRes);
		} catch (FileNotFoundException fnx) {
			JOptionPane.showMessageDialog(null, fnx.getMessage(), "FileNotFoundException", JOptionPane.ERROR_MESSAGE);
		} catch (IOException iox) {
			JOptionPane.showMessageDialog(null, iox.getMessage(), "IOException", JOptionPane.ERROR_MESSAGE);
		}
		taQs.add(Box.createVerticalGlue());
		JScrollPane sptaQs = new JScrollPane(taQs);
		JPanel brdASP = GUIHelper.makeBorder(sptaQs, "Available Queries");
		brdASP.setVisible(true);

		/* Fix for solverL being too tall */
		// Dimension solverLd = solverL.getPreferredSize();
		// solverLd.height=runB.getPreferredSize().height;
		// solverL.setMaximumSize(solverLd);

		JPanel pan;

		pan = new JPanel();
		pan.setLayout(new BoxLayout(pan, BoxLayout.X_AXIS));
		pan.add(new JLabel("    "));
		pan.add(brdASP);
		rightpan.add(pan);

		JButton quitB = new JButton("Exit");
		quitB.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});

		pan = new JPanel();
		pan.setLayout(new BoxLayout(pan, BoxLayout.X_AXIS));
//		pan.add(solverL);
//		pan.add(new JLabel("    "));
//		pan.add(runB);
//		pan.add(new JLabel("    "));
		pan.add(progressBar);
		pan.add(new JLabel("    "));
		pan.add(quitB);

		rightpan.add(pan);
//		rightpan.add(GUIHelper.makeBorder(spRes,"Result"));

		JSplitPane splitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, rightpan,
				GUIHelper.makeBorder(spRes, "Result"));
		// splitPane.setOneTouchExpandable(true);

		guiFrame.add(splitPane, BorderLayout.CENTER);

		// make sure the JFrame is visible
		guiFrame.setVisible(true);

		splitPane.setDividerLocation(0.50); /* split at 50%. Must be done after the split pane is made visible */
	}
}

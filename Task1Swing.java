import java.awt.*;
import javax.swing.*;

public class Task1Swing {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Task1Swing::createUI);
    }

    private static void createUI() {
        JFrame frame = new JFrame("Swing demo — Dzhanteliev EEAIR24");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 320);
        frame.setLocationRelativeTo(null);
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(5, 5, 5, 5);

        JLabel title = new JLabel("Student form");
        title.setFont(new Font("Arial", Font.BOLD, 18));
        c.gridx = 0; c.gridy = 0; c.gridwidth = 2;
        panel.add(title, c);

        c.gridwidth = 1; c.anchor = GridBagConstraints.EAST;
        c.gridx = 0; c.gridy = 1;
        panel.add(new JLabel("Name:"), c);
        JTextField nameField = new JTextField(18);
        c.gridx = 1; c.anchor = GridBagConstraints.WEST;
        panel.add(nameField, c);

        c.gridx = 0; c.gridy = 2; c.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("Group:"), c);
        JTextField groupField = new JTextField(18);
        c.gridx = 1; c.anchor = GridBagConstraints.WEST;
        panel.add(groupField, c);

        c.gridx = 0; c.gridy = 3; c.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("Language:"), c);
        JComboBox<String> langBox = new JComboBox<>(new String[]{"Python", "Java", "JavaScript"});
        c.gridx = 1; c.anchor = GridBagConstraints.WEST;
        panel.add(langBox, c);

        JButton submit = new JButton("Submit");
        JButton clear = new JButton("Clear");
        JPanel buttons = new JPanel();
        buttons.add(submit);
        buttons.add(clear);
        c.gridx = 0; c.gridy = 4; c.gridwidth = 2; c.anchor = GridBagConstraints.CENTER;
        panel.add(buttons, c);

        JLabel result = new JLabel(" ");
        result.setForeground(Color.BLUE);
        c.gridy = 5;
        panel.add(result, c);

        submit.addActionListener(e -> {
            String name = nameField.getText().trim();
            String group = groupField.getText().trim();
            if (name.isEmpty() || group.isEmpty()) {
                JOptionPane.showMessageDialog(frame, "Please fill in both name and group.",
                        "Empty field", JOptionPane.WARNING_MESSAGE);
                return;
            }
            result.setText("<html>Hello, " + name + " from " + group + "!<br>Favourite language: "
                    + langBox.getSelectedItem() + "</html>");
        });

        clear.addActionListener(e -> {
            nameField.setText("");
            groupField.setText("");
            result.setText(" ");
            nameField.requestFocus();
        });

        frame.getRootPane().setDefaultButton(submit);

        frame.add(panel);
        frame.setVisible(true);
    }
}

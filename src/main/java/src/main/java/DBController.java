package main.java;

import com.jfoenix.controls.*;
import com.jfoenix.controls.cells.editors.TextFieldEditorBuilder;
import com.jfoenix.controls.cells.editors.base.GenericEditableTreeTableCell;
import com.jfoenix.controls.datamodels.treetable.RecursiveTreeObject;
import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import javafx.beans.property.ObjectProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TreeTableCell;
import javafx.scene.control.TreeTableColumn;

import java.io.IOException;
import java.security.SecureRandom;
import java.util.Random;
import io.datafx.controller.ViewController;

import javax.annotation.PostConstruct;
import java.util.function.Function;

import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import org.json.*;

import main.java.Connector;

@ViewController(value = "/fxml/ui/TreeTableView.fxml", title = "Material Design Example")
public class DBController {

    //PSQL Variables
    @FXML
    private JFXTreeTableView<Student> editableTreeTableView;

    @FXML
    private JFXTreeTableColumn<Student, ImageView> pictureColumn;

    @FXML
    private JFXTreeTableColumn<Student, String> usernameColumn;

    @FXML
    private JFXTreeTableColumn<Student, String> emailColumn;

    @FXML
    private JFXButton testButton;

    @FXML
    private Label errorLabel;

    @FXML
    private JFXTextField usernameCreate;
    @FXML
    private JFXTextField emailCreate;
    @FXML
    private JFXTextField linkCreate;

    private final String[] names = {"Morley", "Scott", "Kruger", "Lain",
            "Kennedy", "Gawron", "Han", "Hall", "Aydogdu", "Grace",
            "Spiers", "Perera", "Smith", "Connoly",
            "Sokolowski", "Chaow", "James", "June",};

    private final Random random = new SecureRandom();

    private Connector connector = new Connector("http://localhost:5000");

    @FXML
    protected void initialize(){
        setupEditableTableView();
    }

    @FXML
    private void onSend(){
        try {
            this.connector.create(emailCreate.getText(), usernameCreate.getText(), linkCreate.getText());
            this.setupEditableTableView();
        } catch (IOException e) {
            this.errorLabel.setText("Could not create User");
            e.printStackTrace();
        }
    }

    @PostConstruct
    public void init() {
        setupEditableTableView();
    }

    @FXML
    public void onDelete(){
        Student s = editableTreeTableView.getSelectionModel().getSelectedItem().getValue();
        try {
            this.connector.delete(s.emailProperty().getValue());
            this.setupEditableTableView();
        } catch (IOException e) {
            this.errorLabel.setText("Could not delete user due to connection issues");
            e.printStackTrace();
        }
    }

    private void setupEditableTableView() {
        setupCellValueFactory(usernameColumn, Student::usernameProperty);
        setupCellValueFactory(emailColumn, Student::emailProperty);
        //setupCellValueFactory(pictureColumn, Student::pictureProperty);

        // add editors
        usernameColumn.setCellFactory((TreeTableColumn<Student, String> param) -> {
            return new GenericEditableTreeTableCell<>(
                    new TextFieldEditorBuilder());
        });
        usernameColumn.setOnEditCommit((TreeTableColumn.CellEditEvent<Student, String> t) -> {
            Student student = t.getTreeTableView().getTreeItem(t.getTreeTablePosition().getRow()).getValue();
            String email = student.emailProperty().getValue();
            String username = t.getNewValue();
            System.out.println("Edited Username at "+email);

            try {
                this.connector.update(email, username);
                student.usernameProperty().set(username);
            } catch (IOException e) {
                errorLabel.setText("UPDATING STUDENT FAILED");
                e.printStackTrace();
            }
        });

        emailColumn.setCellFactory((TreeTableColumn<Student, String> param) -> {
            return new GenericEditableTreeTableCell<>(
                    new TextFieldEditorBuilder());
        });
        /*emailColumn.setOnEditCommit((TreeTableColumn.CellEditEvent<Student, String> t) -> {
            t.getTreeTableView()
                    .getTreeItem(t.getTreeTablePosition()
                            .getRow())
                    .getValue().emailProperty().set(t.getNewValue());
            System.out.println("Edited Email");
        });*/
        emailColumn.setEditable(false);

        editableTreeTableView.setOnKeyReleased(event -> {
            Object o = event.getSource();
            System.out.println(editableTreeTableView.getSelectionModel().getSelectedItem());
        });



        editableTreeTableView.setOnContextMenuRequested(event -> {
            Object o = event.getPickResult().getIntersectedNode().getParent();

            JFXTreeTableRow row = null;

            if(o instanceof JFXTreeTableRow){
                row = (JFXTreeTableRow) o;
            }else if(o instanceof GenericEditableTreeTableCell){
                row = (JFXTreeTableRow)((GenericEditableTreeTableCell) o).getParent();
            }else{
                row = (JFXTreeTableRow) ((javafx.scene.Group)o).getChildren().toArray()[0];
            }

            Student student = (Student) row.getItem();
            System.out.println(student.emailProperty().getValue());
        });

        //pictureColumn.setCellValueFactory(param -> param.getValue().getValue().picture);

        final ObservableList<Student> students = getStudents();
        editableTreeTableView.setRoot(new RecursiveTreeItem<>(students, RecursiveTreeObject::getChildren));
        editableTreeTableView.setShowRoot(false);
        editableTreeTableView.setEditable(true);
        /*editableTreeTableViewCount.textProperty()
                .bind(Bindings.createStringBinding(() -> PREFIX + editableTreeTableView.getCurrentItemsCount() + POSTFIX,
                        editableTreeTableView.currentItemsCountProperty()));
        searchField2.textProperty()
                .addListener(setupSearchField(editableTreeTableView));*/
    }

    private <T> void setupCellValueFactory(JFXTreeTableColumn<Student, T> column, Function<Student, ObservableValue<T>> mapper) {
        column.setCellValueFactory((TreeTableColumn.CellDataFeatures<Student, T> param) -> {
            if (column.validateValue(param)) {
                return mapper.apply(param.getValue().getValue());
            } else {
                return column.getComputedValue(param);
            }
        });
    }

    private ObservableList<Student> getStudents() {

        try{
            JSONArray arr = new JSONArray(connector.get());
            final ObservableList<Student> dummyData = FXCollections.observableArrayList();
            for(Object a: arr){
                dummyData.add(new Student((String)((JSONObject) a).get("email"), (String)((JSONObject) a).get("username")/*, new ImageView()*/));
            }
            return dummyData;
        }catch(Exception e){
            errorLabel.setText("LOADING STUDENT DATA FAILED");
            e.printStackTrace();
        }


        return null;
    }

    static final class Student extends RecursiveTreeObject<Student> {
        final StringProperty username;
        final StringProperty email;
        //final ImageView picture;

        Student(String email, String username/*, ImageView picture*/) {
            this.email = new SimpleStringProperty(email);
            this.username = new SimpleStringProperty(username);
            /*this.picture = picture;*/
        }

        StringProperty usernameProperty() {
            return username;
        }

        StringProperty emailProperty() {
            return email;
        }

        /*ImageView pictureProperty() {
            return picture;
        }*/
    }

    @FXML
    private void test(){
        /*ObservableList<Student> students = FXCollections.observableArrayList();
        students.add(new Student("asddssaddas", "21"));
        students.add(new Student("asddsasadsad", "28"));
        final TreeItem<Student> root = new RecursiveTreeItem<>(students, RecursiveTreeObject::getChildren);
        editableTreeTableView.setRoot(root);
        editableTreeTableView.setShowRoot(false);
        */

        setupEditableTableView();
        System.out.println("Data loaded");
    }



    private ChangeListener<String> setupSearchField(final JFXTreeTableView<Student> tableView) {
        return (o, oldVal, newVal) ->
                tableView.setPredicate(studentProp -> {
                    final Student student = studentProp.getValue();
                    return student.username.get().contains(newVal)
                            || student.email.get().contains(newVal);
                });
    }
}
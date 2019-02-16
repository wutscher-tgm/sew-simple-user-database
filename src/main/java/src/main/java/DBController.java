package main.java;

import com.jfoenix.controls.*;
import com.jfoenix.controls.cells.editors.TextFieldEditorBuilder;
import com.jfoenix.controls.cells.editors.base.GenericEditableTreeTableCell;
import com.jfoenix.controls.datamodels.treetable.RecursiveTreeObject;

import io.datafx.controller.ViewController;

import javafx.scene.input.KeyCode;
import org.json.*;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.image.ImageView;
import javafx.scene.layout.StackPane;
import javafx.scene.control.TreeTableColumn;

import java.io.IOException;
import java.util.function.Function;


@ViewController(value = "/fxml/ui/TreeTableView.fxml", title = "Material Design Example")
public class DBController {

    @FXML
    private JFXTreeTableView<Student> editableTreeTableView;

    @FXML
    private JFXTreeTableColumn<Student, ImageView> pictureColumn;

    @FXML
    private JFXTreeTableColumn<Student, String> usernameColumn,emailColumn;

    @FXML
    private JFXTextField usernameCreate,emailCreate,linkCreate;

    @FXML
    private JFXDialog dialog;

    @FXML
    private StackPane root;

    @FXML
    private Label errorDialogText;

    private Connector connector = new Connector("http://localhost:5000");

    @FXML
    protected void initialize(){
        setupEditableTableView();
    }

    @FXML
    public void onMessageClose(){
        dialog.close();
    }

    private void showErrorWindow(String content){
        errorDialogText.setText(content);
        dialog.setTransitionType(JFXDialog.DialogTransition.CENTER);
        dialog.setDialogContainer(root);
        dialog.show();
    }

    @FXML
    private void onReload(){
        setupEditableTableView();
        System.out.println("Data loaded");
    }

    @FXML
    private void onSend(){
        try {
            this.connector.create(emailCreate.getText(), usernameCreate.getText(), linkCreate.getText());
            this.setupEditableTableView();
        } catch (IOException e) {
            showErrorWindow("Could not create user due to connection issues");
            e.printStackTrace();
        }
    }

    @FXML
    public void onDelete(){
        try{
            Student s = editableTreeTableView.getSelectionModel().getSelectedItem().getValue();
            this.deleteStudent(s);
        }catch(NullPointerException e){
            showErrorWindow("Please select the user you want to delete in the table above.");
            e.printStackTrace();
        }
    }

    private void deleteStudent(Student s){
        try {
            this.connector.delete(s.emailProperty().getValue());
            this.setupEditableTableView();
        } catch (IOException e) {
            showErrorWindow("Could not delete user due to connection issues");
            e.printStackTrace();
        }
    }

    private void setupEditableTableView() {
        setupCellValueFactory(usernameColumn, Student::usernameProperty);
        setupCellValueFactory(emailColumn, Student::emailProperty);
        //setupCellValueFactory(pictureColumn, Student::pictureProperty);

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
                showErrorWindow("Could not update user due to connection issues");
                e.printStackTrace();
            }
        });

        emailColumn.setCellFactory((TreeTableColumn<Student, String> param) -> {
            return new GenericEditableTreeTableCell<>(
                    new TextFieldEditorBuilder());
        });
        emailColumn.setEditable(false);

        editableTreeTableView.setOnKeyReleased(event -> {
            if(event.getCode() == KeyCode.DELETE || event.getCode() == KeyCode.BACK_SPACE){
                try{
                    Student s = editableTreeTableView.getSelectionModel().getSelectedItem().getValue();
                    this.deleteStudent(s);
                }catch(NullPointerException e){
                    showErrorWindow("Please select the user you want to delete in the table above.");
                    e.printStackTrace();
                }
            }
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
        }catch(IOException e){
            showErrorWindow("Could not load users due to connection issues");
            e.printStackTrace();
            return null;
        }
    }

    static final class Student extends RecursiveTreeObject<Student> {
        final StringProperty username;
        final StringProperty email;

        Student(String email, String username) {
            this.email = new SimpleStringProperty(email);
            this.username = new SimpleStringProperty(username);
        }

        StringProperty usernameProperty() {
            return username;
        }

        StringProperty emailProperty() {
            return email;
        }
    }
}
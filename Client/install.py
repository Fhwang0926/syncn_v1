from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
        QVBoxLayout, QWizard, QWizardPage)


def createIntroPage():
    page = QWizardPage()
    page.setTitle("Introduction")

    label = QLabel(
            "Hello, Dear! We Provide Sticky Note Sync on windows PC\n"
            "You can sync anywhere!!\n"
            "We Not using Database So we don't save your private data anything\n"
            "Before you typing your populor email\n"
            "Is Okay?\n"
            )
    label.setWordWrap(True)

    layout = QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


def createRegistrationPage():
    page = QWizardPage()
    page.setTitle("Auth")
    page.setSubTitle("Please fill E-mail.")

    emailLabel = QLabel("Email address:")
    emailLineEdit = QLineEdit()

    layout = QGridLayout()
    layout.addWidget(emailLabel, 1, 0)
    layout.addWidget(emailLineEdit, 1, 1)
    page.setLayout(layout)

    return page


def createConclusionPage():
    page = QWizardPage()
    page.setTitle("Great!! install Finished!")

    label = QLabel(
        "Once you have completed email authentication on another PC\nyour notes will be synchronized.\n"
    )
    label.setWordWrap(True)

    layout = QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    return page


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    wizard = QWizard()
    wizard.addPage(createIntroPage())
    wizard.addPage(createRegistrationPage())
    wizard.addPage(createConclusionPage())

    wizard.setWindowTitle("SycnN Install Helper")
    wizard.show()

    sys.exit(app.exec_())

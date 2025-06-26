#include <QApplication>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QKeyEvent>
#include <QRandomGenerator>
#include "adasdisplay.h"

ADASDisplay::ADASDisplay(QWidget *parent)
    : QWidget(parent)
{
    setWindowTitle("ADAS Display");
    setWindowState(Qt::WindowFullScreen); // Make it full screen
    setStyleSheet("background-color: #1a1a1a; color: #e0e0e0;"); // Dark theme

    stackedWidget = new QStackedWidget(this);
    initUI();

    currentModeIndex = 0;
    modes << "dashboard" << "rear_view" << "navigation";
    updateDisplayMode();

    // Simulate data updates
    timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &ADASDisplay::updateSimulatedData);
    timer->start(1000); // Update every 1 second

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    mainLayout->addWidget(stackedWidget);
}

ADASDisplay::~ADASDisplay()
{
}

void ADASDisplay::initUI()
{
    // --- Dashboard Mode ---
    dashboardPage = new QWidget();
    QVBoxLayout *dashboardLayout = new QVBoxLayout(dashboardPage);
    dashboardLayout->setContentsMargins(20, 20, 20, 20);
    dashboardLayout->setSpacing(10);

    // Top section: Critical Warnings (LDW, BSD)
    QHBoxLayout *topWarningLayout = new QHBoxLayout();
    ldwLabel = new QLabel("LDW: OK");
    bsdLabel = new QLabel("BSD: OK");
    ldwLabel->setFont(QFont("Arial", 24, QFont::Bold));
    bsdLabel->setFont(QFont("Arial", 24, QFont::Bold));
    ldwLabel->setAlignment(Qt::AlignCenter);
    bsdLabel->setAlignment(Qt::AlignCenter);
    topWarningLayout->addWidget(ldwLabel);
    topWarningLayout->addWidget(bsdLabel);
    dashboardLayout->addLayout(topWarningLayout);

    // Middle section: Speed (Cruise Control)
    speedLabel = new QLabel("SPEED: 0 km/h");
    speedLabel->setFont(QFont("Arial", 72, QFont::Bold));
    speedLabel->setAlignment(Qt::AlignCenter);
    dashboardLayout->addWidget(speedLabel);

    // Bottom section: TSR, Auto Light
    QHBoxLayout *bottomInfoLayout = new QHBoxLayout();
    tsrLabel = new QLabel("TSR: No Sign");
    autoLightLabel = new QLabel("Auto Light: OFF");
    tsrLabel->setFont(QFont("Arial", 24));
    autoLightLabel->setFont(QFont("Arial", 24));
    tsrLabel->setAlignment(Qt::AlignCenter);
    autoLightLabel->setAlignment(Qt::AlignCenter);
    bottomInfoLayout->addWidget(tsrLabel);
    bottomInfoLayout->addWidget(autoLightLabel);
    dashboardLayout->addLayout(bottomInfoLayout);

    stackedWidget->addWidget(dashboardPage); // Index 0

    // --- Rear View Camera Mode ---
    rearViewPage = new QWidget();
    QVBoxLayout *rearViewLayout = new QVBoxLayout(rearViewPage);
    rearViewLabel = new QLabel("REAR VIEW CAMERA FEED");
    rearViewLabel->setFont(QFont("Arial", 48, QFont::Bold));
    rearViewLabel->setAlignment(Qt::AlignCenter);
    rearViewLayout->addWidget(rearViewLabel);
    stackedWidget->addWidget(rearViewPage); // Index 1

    // --- Navigation Mode ---
    navigationPage = new QWidget();
    QVBoxLayout *navigationLayout = new QVBoxLayout(navigationPage);
    navigationLabel = new QLabel("RACE NAVIGATION MAP");
    navigationLabel->setFont(QFont("Arial", 48, QFont::Bold));
    navigationLabel->setAlignment(Qt::AlignCenter);
    lapCounterLabel = new QLabel("LAP: 0/0");
    lapCounterLabel->setFont(QFont("Arial", 36));
    lapCounterLabel->setAlignment(Qt::AlignCenter);
    navigationLayout->addWidget(navigationLabel);
    navigationLayout->addWidget(lapCounterLabel);
    stackedWidget->addWidget(navigationPage); // Index 2
}

void ADASDisplay::updateDisplayMode()
{
    stackedWidget->setCurrentIndex(currentModeIndex);
}

void ADASDisplay::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Right) { // Simulate "Forward" button
        currentModeIndex = (currentModeIndex + 1) % modes.size();
        updateDisplayMode();
    } else if (event->key() == Qt::Key_Left) { // Simulate "Backward" button
        currentModeIndex = (currentModeIndex - 1 + modes.size()) % modes.size();
        updateDisplayMode();
    } else if (event->key() == Qt::Key_Q) { // Quit
        close();
    }
}

void ADASDisplay::updateSimulatedData()
{
    if (currentModeIndex == 0) { // Only update dashboard elements in dashboard mode
        // Simulate LDW/BSD warnings
        if (QRandomGenerator::global()->generateDouble() < 0.1) { // 10% chance of warning
            ldwLabel->setText("LDW: WARNING!");
            ldwLabel->setStyleSheet("color: red; font-weight: bold;");
        } else {
            ldwLabel->setText("LDW: OK");
            ldwLabel->setStyleSheet("color: #e0e0e0;");
        }

        if (QRandomGenerator::global()->generateDouble() < 0.05) { // 5% chance of BSD warning
            bsdLabel->setText("BSD: OBJECT!");
            bsdLabel->setStyleSheet("color: orange; font-weight: bold;");
        } else {
            bsdLabel->setText("BSD: OK");
            bsdLabel->setStyleSheet("color: #e0e0e0;");
        }

        // Simulate speed (Cruise Control)
        int currentSpeed = QRandomGenerator::global()->bounded(60, 121); // 60 to 120
        speedLabel->setText(QString("SPEED: %1 km/h").arg(currentSpeed));

        // Simulate TSR
        QStringList signs = {"No Sign", "Speed 50", "Stop Sign", "Yield"};
        tsrLabel->setText(QString("TSR: %1").arg(signs.at(QRandomGenerator::global()->bounded(signs.size()))));

        // Simulate Auto Light
        QString lightStatus = (QRandomGenerator::global()->generateDouble() < 0.5) ? "ON" : "OFF";
        autoLightLabel->setText(QString("Auto Light: %1").arg(lightStatus));
    }
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ADASDisplay w;
    w.show();
    return a.exec();
}

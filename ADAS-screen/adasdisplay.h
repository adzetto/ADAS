#ifndef ADASDISPLAY_H
#define ADASDISPLAY_H

#include <QWidget>
#include <QLabel>
#include <QStackedWidget>
#include <QTimer>

class ADASDisplay : public QWidget
{
    Q_OBJECT

public:
    ADASDisplay(QWidget *parent = nullptr);
    ~ADASDisplay();

protected:
    void keyPressEvent(QKeyEvent *event) override;

private slots:
    void updateSimulatedData();

private:
    void initUI();
    void updateDisplayMode();

    QStackedWidget *stackedWidget;
    QWidget *dashboardPage;
    QLabel *ldwLabel;
    QLabel *bsdLabel;
    QLabel *speedLabel;
    QLabel *tsrLabel;
    QLabel *autoLightLabel;

    QWidget *rearViewPage;
    QLabel *rearViewLabel;

    QWidget *navigationPage;
    QLabel *navigationLabel;
    QLabel *lapCounterLabel;

    QTimer *timer;
    int currentModeIndex;
    QStringList modes;
};
#endif // ADASDISPLAY_H

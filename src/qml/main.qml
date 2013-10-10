import QtQuick 1.1

Item {
	id: container;
	width: 600; 
	
	Rectangle {
		radius: 5
		opacity: 0.6
		color: "#2d2d2d"
		anchors.fill: parent
		smooth: true
	}
	
	Rectangle {
		radius: 5
		color: "#FFFFFF"
		anchors.fill: parent
		anchors.margins: 6
		smooth: true
	}
	
	SearchBox {
		anchors.horizontalCenter: container.horizontalCenter
		anchors.top: parent.top
		anchors.topMargin: 12
		width: container.width - 30; height: 30
	}
	
	
}
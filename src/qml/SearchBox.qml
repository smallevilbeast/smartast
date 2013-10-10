import QtQuick 1.1

Item {
	
	id: container
	property alias text: textInput.text
	
	Rectangle {
		
		border { width: 1; color: "#bfbfbf"}
		color: "#F9F9F9"
		anchors.fill: parent
		smooth: true
	}
	
	TextInput {
		id: textInput
		selectByMouse: true
		anchors.fill: parent
		width: parent.width
		anchors.margins: 5
		smooth: true
	}
	
	ListModel {
		id: suggestModel
		
		ListElement { keyword: "Linux"; desc: "這是最新版的深度音樂哈!" }
		ListElement { keyword: "Linux"; desc: "這是最新版的深度音樂哈!" }
		ListElement { keyword: "Linux"; desc: "這是最新版的深度音樂哈!" }
		
		ListElement { keyword: "deepin"; desc: "我鑤了" }
	}
	
	ListView {
		id: suggest
				
		width: parent.width; height: 320
		anchors.top: parent.bottom
		interactive: true
		clip: true
		model: suggestModel
		delegate: SuggestDelegate {}
	}
}

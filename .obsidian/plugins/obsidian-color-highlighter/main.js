const { Plugin, MarkdownView } = require("obsidian");

module.exports = class ColorHighlighterPlugin extends Plugin {
    async onload() {
        console.log("Loading Color Highlighter Plugin");

        // Command: Highlight Green
        this.addCommand({
            id: "highlight-green",
            name: "Highlight Green",
            editorCallback: (editor, view) => {
                const selection = editor.getSelection();
                if (selection) {
                    editor.replaceSelection(`<mark style="background-color: rgba(46, 204, 113, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                }
            }
        });

        // Command: Highlight Orange
        this.addCommand({
            id: "highlight-orange",
            name: "Highlight Orange",
            editorCallback: (editor, view) => {
                const selection = editor.getSelection();
                if (selection) {
                    editor.replaceSelection(`<mark style="background-color: rgba(230, 126, 34, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                }
            }
        });

        // Command: Highlight Yellow
        this.addCommand({
            id: "highlight-yellow",
            name: "Highlight Yellow",
            editorCallback: (editor, view) => {
                const selection = editor.getSelection();
                if (selection) {
                    editor.replaceSelection(`<mark style="background-color: rgba(241, 196, 15, 0.45); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                }
            }
        });

        // Command: Highlight Red
        this.addCommand({
            id: "highlight-red",
            name: "Highlight Red",
            editorCallback: (editor, view) => {
                const selection = editor.getSelection();
                if (selection) {
                    editor.replaceSelection(`<mark style="background-color: rgba(231, 76, 60, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                }
            }
        });

        // Intercept literal 'g', 'o', 'y', and 'r' keys when there is an active selection in the editor
        this.registerDomEvent(document, 'keydown', (event) => {
            // Skip if any modifier keys are pressed
            if (event.ctrlKey || event.altKey || event.metaKey || event.shiftKey) {
                return;
            }

            if (event.key !== 'g' && event.key !== 'o' && event.key !== 'y' && event.key !== 'r') {
                return;
            }

            // Verify the focus is inside a Markdown editor body
            const activeEl = document.activeElement;
            if (activeEl) {
                const tagName = activeEl.tagName.toLowerCase();
                if (tagName === 'input' || tagName === 'textarea') {
                    return;
                }
                if (!activeEl.classList.contains('cm-content')) {
                    return;
                }
            }

            // Get the active Markdown view
            const markdownView = this.app.workspace.getActiveViewOfType(MarkdownView);
            if (!markdownView) {
                return;
            }

            const editor = markdownView.editor;
            const selection = editor.getSelection();

            // If there's an active text selection, highlight it and prevent default key typing behavior
            if (selection && selection.length > 0) {
                event.preventDefault();
                event.stopPropagation();

                if (event.key === 'g') {
                    editor.replaceSelection(`<mark style="background-color: rgba(46, 204, 113, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                } else if (event.key === 'o') {
                    editor.replaceSelection(`<mark style="background-color: rgba(230, 126, 34, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                } else if (event.key === 'y') {
                    editor.replaceSelection(`<mark style="background-color: rgba(241, 196, 15, 0.45); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                } else if (event.key === 'r') {
                    editor.replaceSelection(`<mark style="background-color: rgba(231, 76, 60, 0.4); color: inherit; padding: 0.1em 0.2em; border-radius: 0.2em;">${selection}</mark>`);
                }
            }
        });
    }

    onunload() {
        console.log("Unloading Color Highlighter Plugin");
    }
};

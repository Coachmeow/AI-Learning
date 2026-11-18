// CodeMirror editor for hands-on exercises (loaded only when the Hands-on tab opens).
import { EditorView, basicSetup } from 'codemirror';
import { indentWithTab } from '@codemirror/commands';
import { indentUnit } from '@codemirror/language';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { keymap } from '@codemirror/view';

export function createEditor(parent: HTMLElement, doc: string, onChange: (text: string) => void) {
  const view = new EditorView({
    doc,
    parent,
    extensions: [
      basicSetup,
      keymap.of([indentWithTab]),
      indentUnit.of('    '),
      python(),
      oneDark,
      EditorView.contentAttributes.of({ 'aria-label': 'solution.py', spellcheck: 'false' }),
      EditorView.updateListener.of((u) => {
        if (u.docChanged) onChange(u.state.doc.toString());
      }),
    ],
  });
  return {
    get: () => view.state.doc.toString(),
    set: (text: string) => view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } }),
  };
}

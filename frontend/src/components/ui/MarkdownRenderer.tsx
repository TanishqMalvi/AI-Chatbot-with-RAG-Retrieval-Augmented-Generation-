import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  const memoizedContent = useMemo(() => content, [content]);

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({ inline, className, children, ...props }: any) {
          const match = /language-(\w+)/.exec(className || '');
          const language = match ? match[1] : 'text';

          if (inline) {
            return (
              <code
                style={{
                  background: 'rgba(0,212,255,0.1)',
                  color: '#00D4FF',
                  padding: '2px 6px',
                  borderRadius: '4px',
                  fontFamily: 'var(--font-code)',
                  fontSize: '0.9em',
                }}
                {...props}
              >
                {children}
              </code>
            );
          }

          return (
            <SyntaxHighlighter
              language={language}
              style={atomDark as any}
              customStyle={{
                background: 'rgba(8,12,20,0.8)',
                borderRadius: '8px',
                padding: '12px',
                margin: '8px 0',
                fontSize: '13px',
                border: '1px solid rgba(0,212,255,0.2)',
              }}
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          );
        },
        table({ children }: any) {
          return (
            <div
              style={{
                overflowX: 'auto',
                margin: '12px 0',
                borderRadius: '8px',
                border: '1px solid rgba(0,212,255,0.2)',
              }}
            >
              <table
                style={{
                  borderCollapse: 'collapse',
                  width: '100%',
                  fontSize: '13px',
                }}
              >
                {children}
              </table>
            </div>
          );
        },
        thead({ children }: any) {
          return (
            <thead
              style={{
                background: 'rgba(0,212,255,0.1)',
                borderBottom: '2px solid rgba(0,212,255,0.3)',
              }}
            >
              {children}
            </thead>
          );
        },
        th({ children }: any) {
          return (
            <th
              style={{
                padding: '10px 12px',
                textAlign: 'left',
                fontWeight: 600,
                color: '#00D4FF',
              }}
            >
              {children}
            </th>
          );
        },
        td({ children }: any) {
          return (
            <td
              style={{
                padding: '10px 12px',
                borderBottom: '1px solid rgba(255,255,255,0.08)',
                color: '#CBD5E1',
              }}
            >
              {children}
            </td>
          );
        },
        h1({ children }: any) {
          return (
            <h1
              style={{
                fontSize: '1.75em',
                fontWeight: 700,
                marginTop: '16px',
                marginBottom: '8px',
                color: '#F8FAFC',
              }}
            >
              {children}
            </h1>
          );
        },
        h2({ children }: any) {
          return (
            <h2
              style={{
                fontSize: '1.5em',
                fontWeight: 700,
                marginTop: '14px',
                marginBottom: '8px',
                color: '#F8FAFC',
              }}
            >
              {children}
            </h2>
          );
        },
        h3({ children }: any) {
          return (
            <h3
              style={{
                fontSize: '1.25em',
                fontWeight: 700,
                marginTop: '12px',
                marginBottom: '6px',
                color: '#F8FAFC',
              }}
            >
              {children}
            </h3>
          );
        },
        h4({ children }: any) {
          return (
            <h4
              style={{
                fontSize: '1.1em',
                fontWeight: 600,
                marginTop: '10px',
                marginBottom: '6px',
                color: '#F8FAFC',
              }}
            >
              {children}
            </h4>
          );
        },
        h5({ children }: any) {
          return (
            <h5
              style={{
                fontSize: '1em',
                fontWeight: 600,
                marginTop: '8px',
                marginBottom: '4px',
                color: '#F8FAFC',
              }}
            >
              {children}
            </h5>
          );
        },
        h6({ children }: any) {
          return (
            <h6
              style={{
                fontSize: '0.95em',
                fontWeight: 600,
                marginTop: '8px',
                marginBottom: '4px',
                color: '#CBD5E1',
              }}
            >
              {children}
            </h6>
          );
        },
        p({ children }: any) {
          return (
            <p
              style={{
                marginBottom: '8px',
                lineHeight: 1.7,
                color: '#CBD5E1',
              }}
            >
              {children}
            </p>
          );
        },
        ul({ children }: any) {
          return (
            <ul
              style={{
                marginLeft: '20px',
                marginBottom: '8px',
                listStyle: 'disc',
              }}
            >
              {children}
            </ul>
          );
        },
        ol({ children }: any) {
          return (
            <ol
              style={{
                marginLeft: '20px',
                marginBottom: '8px',
                listStyle: 'decimal',
              }}
            >
              {children}
            </ol>
          );
        },
        li({ children }: any) {
          return (
            <li
              style={{
                marginBottom: '4px',
                color: '#CBD5E1',
              }}
            >
              {children}
            </li>
          );
        },
        blockquote({ children }: any) {
          return (
            <blockquote
              style={{
                borderLeft: '4px solid rgba(0,212,255,0.3)',
                paddingLeft: '12px',
                marginLeft: 0,
                marginBottom: '8px',
                color: '#94A3B8',
                fontStyle: 'italic',
              }}
            >
              {children}
            </blockquote>
          );
        },
        strong({ children }: any) {
          return (
            <strong style={{ color: '#00D4FF', fontWeight: 600 }}>
              {children}
            </strong>
          );
        },
        em({ children }: any) {
          return (
            <em style={{ color: '#CBD5E1', fontStyle: 'italic' }}>
              {children}
            </em>
          );
        },
        a({ href, children }: any) {
          return (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: '#00D4FF',
                textDecoration: 'none',
                borderBottom: '1px solid rgba(0,212,255,0.3)',
                transition: 'all 0.2s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderBottomColor = 'rgba(0,212,255,0.8)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderBottomColor = 'rgba(0,212,255,0.3)';
              }}
            >
              {children}
            </a>
          );
        },
        hr() {
          return (
            <hr
              style={{
                border: 'none',
                height: '1px',
                background: 'rgba(255,255,255,0.1)',
                margin: '12px 0',
              }}
            />
          );
        },
      }}
    >
      {memoizedContent}
    </ReactMarkdown>
  );
};

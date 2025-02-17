import { Html, Head, Main, NextScript } from "next/document";

export default function MyDocument() {
    return (
        <Html lang="pt-BR">
            <Head>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                {/*<link rel="icon" href="/favicon.ico" />*/}
            </Head>
            <body className="bg-gray-100">
                <Main />
                <NextScript />
            </body>
        </Html>
    );
}
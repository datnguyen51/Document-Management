def format_html_mail_register(username, password):
    html = """
        <head>
        <style type="text/css">
            #outlook a {
                padding: 0;
            }

            .ExternalClass {
                width: 100%;
            }

            .ExternalClass,
            .ExternalClass p,
            .ExternalClass span,
            .ExternalClass font,
            .ExternalClass td,
            .ExternalClass div {
                line-height: 100%;
            }

            .es-button {
                mso-style-priority: 100 !important;
                text-decoration: none !important;
            }

            a[x-apple-data-detectors] {
                color: inherit !important;
                text-decoration: none !important;
                font-size: inherit !important;
                font-family: inherit !important;
                font-weight: inherit !important;
                line-height: inherit !important;
            }

            .es-desk-hidden {
                display: none;
                float: left;
                overflow: hidden;
                width: 0;
                max-height: 0;
                line-height: 0;
                mso-hide: all;
            }

            .es-button-border:hover a.es-button,
            .es-button-border:hover button.es-button {
                background: #ffffff !important;
                border-color: #ffffff !important;
            }

            .es-button-border:hover {
                background: #ffffff !important;
                border-style: solid solid solid solid !important;
                border-color: #3d5ca3 #3d5ca3 #3d5ca3 #3d5ca3 !important;
            }

            [data-ogsb] .es-button {
                border-width: 0 !important;
                padding: 15px 20px 15px 20px !important;
            }

            @media only screen and (max-width:600px),
            screen and (max-device-width:600px) {

                p,
                ul li,
                ol li,
                a {
                    line-height: 150% !important
                }

                h1,
                h2,
                h3,
                h1 a,
                h2 a,
                h3 a {
                    line-height: 120% !important
                }

                h1 {
                    font-size: 20px !important;
                    text-align: center
                }

                h2 {
                    font-size: 16px !important;
                    text-align: left
                }

                h3 {
                    font-size: 20px !important;
                    text-align: center
                }

                .es-header-body h1 a,
                .es-content-body h1 a,
                .es-footer-body h1 a {
                    font-size: 20px !important
                }

                h2 a {
                    text-align: left
                }

                .es-header-body h2 a,
                .es-content-body h2 a,
                .es-footer-body h2 a {
                    font-size: 16px !important
                }

                .es-header-body h3 a,
                .es-content-body h3 a,
                .es-footer-body h3 a {
                    font-size: 20px !important
                }

                .es-menu td a {
                    font-size: 14px !important
                }

                .es-header-body p,
                .es-header-body ul li,
                .es-header-body ol li,
                .es-header-body a {
                    font-size: 10px !important
                }

                .es-content-body p,
                .es-content-body ul li,
                .es-content-body ol li,
                .es-content-body a {
                    font-size: 16px !important
                }

                .es-footer-body p,
                .es-footer-body ul li,
                .es-footer-body ol li,
                .es-footer-body a {
                    font-size: 12px !important
                }

                .es-infoblock p,
                .es-infoblock ul li,
                .es-infoblock ol li,
                .es-infoblock a {
                    font-size: 12px !important
                }

                *[class="gmail-fix"] {
                    display: none !important
                }

                .es-m-txt-c,
                .es-m-txt-c h1,
                .es-m-txt-c h2,
                .es-m-txt-c h3 {
                    text-align: center !important
                }

                .es-m-txt-r,
                .es-m-txt-r h1,
                .es-m-txt-r h2,
                .es-m-txt-r h3 {
                    text-align: right !important
                }

                .es-m-txt-l,
                .es-m-txt-l h1,
                .es-m-txt-l h2,
                .es-m-txt-l h3 {
                    text-align: left !important
                }

                .es-m-txt-r img,
                .es-m-txt-c img,
                .es-m-txt-l img {
                    display: inline !important
                }

                .es-button-border {
                    display: block !important
                }

                a.es-button,
                button.es-button {
                    font-size: 14px !important;
                    display: block !important;
                    border-left-width: 0px !important;
                    border-right-width: 0px !important
                }

                .es-btn-fw {
                    border-width: 10px 0px !important;
                    text-align: center !important
                }

                .es-adaptive table,
                .es-btn-fw,
                .es-btn-fw-brdr,
                .es-left,
                .es-right {
                    width: 100% !important
                }

                .es-content table,
                .es-header table,
                .es-footer table,
                .es-content,
                .es-footer,
                .es-header {
                    width: 100% !important;
                    max-width: 600px !important
                }

                .es-adapt-td {
                    display: block !important;
                    width: 100% !important
                }

                .adapt-img {
                    width: 100% !important;
                    height: auto !important
                }

                .es-m-p0 {
                    padding: 0px !important
                }

                .es-m-p0r {
                    padding-right: 0px !important
                }

                .es-m-p0l {
                    padding-left: 0px !important
                }

                .es-m-p0t {
                    padding-top: 0px !important
                }

                .es-m-p0b {
                    padding-bottom: 0 !important
                }

                .es-m-p20b {
                    padding-bottom: 20px !important
                }

                .es-mobile-hidden,
                .es-hidden {
                    display: none !important
                }

                tr.es-desk-hidden,
                td.es-desk-hidden,
                table.es-desk-hidden {
                    width: auto !important;
                    overflow: visible !important;
                    float: none !important;
                    max-height: inherit !important;
                    line-height: inherit !important
                }

                tr.es-desk-hidden {
                    display: table-row !important
                }

                table.es-desk-hidden {
                    display: table !important
                }

                td.es-desk-menu-hidden {
                    display: table-cell !important
                }

                .es-menu td {
                    width: 1% !important
                }

                table.es-table-not-adapt,
                .esd-block-html table {
                    width: auto !important
                }

                table.es-social {
                    display: inline-block !important
                }

                table.es-social td {
                    display: inline-block !important
                }
            }
        </style>
    </head>

    <body
        style="width:100%;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
        <div class="es-wrapper-color" style="background-color:#FAFAFA">
            <!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"> <v:fill type="tile" color="#fafafa"></v:fill> </v:background><![endif]-->
            <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top">
                <tr style="border-collapse:collapse">
                    <td valign="top" style="padding:0;Margin:0">
                        <table cellpadding="0" cellspacing="0" class="es-header" align="center"
                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
                            <tr style="border-collapse:collapse">
                                <td class="es-adaptive" align="center" style="padding:0;Margin:0">
                                    <table class="es-header-body"
                                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#3d5ca3;width:600px"
                                        cellspacing="0" cellpadding="0" bgcolor="#3d5ca3" align="center">
                                        <tr style="border-collapse:collapse">
                                            <td style="padding:20px;Margin:0;background-color:#0a4da2" bgcolor="#0a4da2"
                                                align="left">
                                                <!--[if mso]><table style="width:560px" cellpadding="0" cellspacing="0"><tr><td style="width:120px" valign="top"><![endif]-->
                                                <table cellspacing="0" cellpadding="0" align="left" class="es-left"
                                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                                                    <tr style="border-collapse:collapse">
                                                        <td class="es-m-p20b" align="left"
                                                            style="padding:0;Margin:0;width:120px">
                                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                                role="presentation"
                                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                <tr style="border-collapse:collapse">
                                                                    <td class="es-m-p0l es-m-txt-c" align="left"
                                                                        style="padding:0;Margin:0;font-size:0px"><a
                                                                            href="https://viewstripo.email" target="_blank"
                                                                            style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:none;color:#1376C8;font-size:14px"><img
                                                                                src="https://lmhcrp.stripocdn.email/content/guids/CABINET_d53d7e4003eec8bde2992dec4a751c48/images/18561629717763943.jpeg"
                                                                                alt
                                                                                style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                                width="120"></a></td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                <!--[if mso]></td><td style="width:20px"></td><td style="width:420px" valign="top"><![endif]-->
                                                <table cellpadding="0" cellspacing="0" class="es-right" align="right"
                                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                                                    <tr style="border-collapse:collapse">
                                                        <td align="left" style="padding:0;Margin:0;width:420px">
                                                            <table cellpadding="0" cellspacing="0" width="100%"
                                                                role="presentation"
                                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-top:10px">
                                                                        <p
                                                                            style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:54px;color:#ffffff;font-size:45px">
                                                                            <strong>Thang Long University</strong></p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                <!--[if mso]></td></tr></table><![endif]-->
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
                            <tr style="border-collapse:collapse">
                                <td style="padding:0;Margin:0;background-color:#fafafa" bgcolor="#fafafa" align="center">
                                    <table class="es-content-body"
                                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#ffffff;width:600px"
                                        cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center">
                                        <tr style="border-collapse:collapse">
                                            <td align="left" bgcolor="#ffffff"
                                                style="padding:0;Margin:0;padding-left:20px;padding-right:20px;padding-top:40px;background-color:#ffffff">
                                                <table width="100%" cellspacing="0" cellpadding="0"
                                                    style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                    <tr style="border-collapse:collapse">
                                                        <td valign="top" align="center"
                                                            style="padding:0;Margin:0;width:560px">
                                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                                role="presentation"
                                                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px;font-size:0px">
                                                                        <img src="https://lmhcrp.stripocdn.email/content/guids/CABINET_d53d7e4003eec8bde2992dec4a751c48/images/25951629724890848.png"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                                                            width="175"></td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-top:15px;padding-bottom:15px">
                                                                        <h1
                                                                            style="Margin:0;line-height:24px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:20px;font-style:normal;font-weight:normal;color:#333333">
                                                                            <b>INFO ACCOUNT</b></h1>
                                                                    </td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-left:40px;padding-right:40px">
                                                                        <p
                                                                            style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                            HI,&nbsp;""" + username + """</p>
                                                                    </td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-top:10px;padding-left:40px;padding-right:40px">
                                                                        <p
                                                                            style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:24px;color:#666666;font-size:16px">
                                                                            Thank you for using, here is your login password
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:20px;Margin:0;font-size:0">
                                                                        <table border="0" width="90%" height="100%"
                                                                            cellpadding="0" cellspacing="0"
                                                                            role="presentation"
                                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                            <tr style="border-collapse:collapse">
                                                                                <td
                                                                                    style="padding:0;Margin:0;border-bottom:1px solid #cccccc;background:none;height:1px;width:100%;margin:0px">
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:0;Margin:0;padding-top:5px;padding-bottom:5px">
                                                                        <p
                                                                            style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;line-height:28px;color:#0a76cd;font-size:23px">
                                                                            <strong>""" + password + """</strong></p>
                                                                    </td>
                                                                </tr>
                                                                <tr style="border-collapse:collapse">
                                                                    <td align="center"
                                                                        style="padding:20px;Margin:0;font-size:0">
                                                                        <table border="0" width="90%" height="100%"
                                                                            cellpadding="0" cellspacing="0"
                                                                            role="presentation"
                                                                            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                                            <tr style="border-collapse:collapse">
                                                                                <td
                                                                                    style="padding:0;Margin:0;border-bottom:1px solid #cccccc;background:none;height:1px;width:100%;margin:0px">
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>
    </body>

    </html>
    """

    return html

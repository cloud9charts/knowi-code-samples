#Example code to use embed Knowi using the JS API.


The JavaScript API is an alternative approach to the iFrame embed method.
#### [Link to official Knowi embedding](https://knowi.com/docs/embedSSO.html)
#### [Official info on JS API](https://knowi.com/docs/embedSSO.html#JavaScriptEmbedAPI)


| parameter | description | possible values | example |
| :----: | :--- | :---- | :---:
| `type` | type of asset to embed | dashboard: `share`, secure dashboard: `secure`, sso: `single`, widget: `shareWidget`, secure widget: `shareWidgetSecure`, nlp: `nlp` | `shareWidget` |
| `dashboard` | share URL of dashboard/widget | - | `4isCHaxEVxxIb9pDfyvnF5tNusQOJlSE8BtLFLh6CEnYie` 
| `dashboardId` | ID of dashboard/widget | - | `123456`
| `hash` | AES encrypted hash for *secure* dashboard/widget. Must be used with type: `secure`, `shareWidgetSecure`  | - | `hKNSyuN9kZTw3xhcXmfiurqsxbPhIKQ5Dplu7PDo840DGbFg3p24hhoV` 
| `token` | session token for single sign on | - | `4isCHaxEVxxIb9pDfyvnF5tNusQOJlSE8BtLFLh6CEnYie`
| `url` | url for on-premise deployments | - | `https://www.knowi.com`
| `view` | customizable options for display | [see below](#viewOptions) | `view: {title: true, resize: true, backgroundColor: 'transparent', scroll: false}`


<a name="viewOptions"></a>
possible `view` configurations

| `view` attribute | description | possible values |
| :----: | :---- | :--- |
| `title` | enable widget title and action menus | `boolean`
| `filter` | enable dashboard/widget filter | `boolean`
| `autoHeight` | automatically adjust dashboard height to div | `boolean`
| `border` | enable borders around widget | `boolean`
| `widgetSpacing` | spacing between widgets (px) | `0-200`
| `setting` | enable widget settings | `boolean`
| `resize` | enable widget on a dashboard to be resized | `boolean`
| `drag` | enable widget on a dashboard to be rearranged | `boolean`
| `scroll` | enable scroll on a dashboard |
| `header` | enable dashboard header including dashboard name, settings, and dashboard filter | `boolean`
| `backgroundColor` | background color of dashboard. | Formats are value: `rebeccapurple`, HEX value: `#92a8d1`, RGB: `rgb(201, 76, 76`, RGBA: `rgba(201, 76, 76, 0.6)` 
| `analytics` | enable Analytics mode for widgets. Applicable for types: *shareWidget*, *shareWidgetSecure* | `boolean`
| `menu` | enable side menu with system actions | `boolean`
| `menuOption` | disable selected side menu. Defaults to show all menu options | `{logo: false, dashboards: false, widgets: false, datasources: false, queries: false, ml: false, settings: false, help: false, logout: false}`
| `css` | array of custom css  | `['https://rawgit.com/AntonLapshin/csharp/master/custom1.css', 'https://rawgit.com/AntonLapshin/csharp/master/custom2.css]`
| `contentFilters` | JSON array to filter content. Applicable for types: *share*, *shareWidget* | `[{"fieldName": "department", "values": ["sales", 19], "operator": "="}, {...}]`


 
const fs = require("fs");
const Handlebars = require("handlebars");

const doc = JSON.parse(fs.readFileSync("./target/doc/bitwarden_uniffi.json", "utf8"));
const command = JSON.parse(
  fs.readFileSync("./support/schemas/bitwarden_json/Command.json", "utf8"),
);

const localIndexArray = Object.values(doc.index).filter((entry) => entry.crate_id == 0);
const localIndex = localIndexArray.reduce(function (map, obj) {
  map[obj.id] = obj;
  return map;
}, {});

const rootElements = ["Client", "ClientKdf", "ClientCrypto"];

let usedDefinitions = [];

const out = rootElements.map((rootElement) => {
  const root = localIndexArray.find((entry) => entry.name == rootElement);
  const impls = root.inner.struct.impls;

  const elements = impls
    .flatMap((e) => localIndex[e])
    .flatMap((e) => e.inner.impl.items)
    .map((e) => localIndex[e])
    .filter((e) => e?.docs != null);

  return {
    name: rootElement,
    elements: elements.map((e) => {
      return {
        name: e.name,
        docs: e.docs,
        args: e.inner.function.decl.inputs.map((e) => map_input(e)),
        output: map_type(e.inner.function.decl.output),
      };
    }),
  };
});

const template = Handlebars.compile(`
# Bitwarden Mobile SDK

{{#each sections}}

## {{name}}

{{#each elements}}
### \`{{name}}\`
{{docs}}

**Arguments**:
{{#each args}}
- {{name}}: {{{type}}}
{{/each}}

**Output**: {{{output}}}

{{/each}}
{{/each}}

# Command references
    
{{#each commands}}

## \`{{@key}}\`

{{#if oneOf}}
<table>
<tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
</tr>
{{#each oneOf}}
{{#each properties}}
<tr>
    <th>{{@key}}</th>
    <th>{{type}}</th>
    <th></th>
</tr>
{{#if properties}}
<tr>
    <td colspan="3">
        <table>
        <tr>
            <th>Key</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
        {{#each properties}}
            <tr>
                <td>{{@key}}</td>
                <td>{{type}}</td>
                <td>{{{description}}}</td>
            </tr>
        {{/each}}
        </table>
    </td>
</tr>
{{/if}}
{{/each}}
{{/each}}
</table>

{{/if}}

{{#unless oneOf}}
<table>
<tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
</tr>
{{#each properties}}
<tr>
    <th>{{@key}}</th>
    <th>{{type}}</th>
    <th>{{description}}</th>
</tr>
{{/each}}
</table>
{{/unless}}

{{/each}}
`);

function stripDef(str) {
  return str.replace(/#\/definitions\//g, "");
}

Handlebars.registerHelper("propertiesTable", function (schema, parentKey) {
  return new Handlebars.SafeString(propertiesTable(schema, parentKey));
});

Handlebars.registerHelper("stripDef", (str) => {
  return stripDef(str);
});

// Add references
for (let i = 0; i < usedDefinitions.length; i++) {
  const key = usedDefinitions[i];
  const cmd = command.definitions[key];
  if (cmd == null) {
    continue;
  }

  Object.entries(cmd.properties ?? {}).forEach((prop) => {
    prop[1].allOf?.forEach((e) => {
      usedDefinitions.push(stripDef(e["$ref"]));
    });
  });
}

const filteredDefinitions = [...new Set(usedDefinitions)]
  .sort()
  .map((key) => [key, command.definitions[key]])
  .filter((e) => e[1] != null)
  .reduce((obj, cur) => ({ ...obj, [cur[0]]: cur[1] }), {});

console.log(template({ sections: out, commands: filteredDefinitions }));

///
/// Implementation details below.
///

// Format
function map_input(input) {
  const t = map_type(input[1]);
  return {
    name: input[0],
    type: t,
  };
}

function map_type(t) {
  const args = t.resolved_path?.args;
  const name = t.resolved_path?.name;

  let out = "";

  if (name) {
    usedDefinitions.push(name);

    if (command.definitions[name] != null) {
      out += `[${name}](#${name})`;
    } else {
      out += name;
    }
  }

  if (args?.angle_bracketed.args.length > 0) {
    out += "<";
    out += args.angle_bracketed.args.map((t) => {
      if (t.type.generic) {
        return t.type.generic;
      } else if (t.type.resolved_path) {
        return t.type.resolved_path.name;
      }
    });
    out += ">";
  }
  return out;
}

# Changelog

## 1.0.0 (2023-10-13)


### 🚀 Features

* add copy_and_replace method ([de87be9](https://github.com/agrc/swapper/commit/de87be989b83606c19ef654385625b9ac90eeaaa))
* add support for an empty destination to swap ([bddb9e5](https://github.com/agrc/swapper/commit/bddb9e5daad67475caf82606f3875c96af51f8d1)), closes [#9](https://github.com/agrc/swapper/issues/9)
* add support for swapping stand alone tables ([2ba9bac](https://github.com/agrc/swapper/commit/2ba9bac5d28e8ecf3ff75b306a4822e97fa9efed))
* implement compare command ([582d902](https://github.com/agrc/swapper/commit/582d9025e26c680241e34b6426ad8f64e9ac5648))
* make package pip-installable ([502c7df](https://github.com/agrc/swapper/commit/502c7df747c48da457cf3472d8c07a71421d1a17))
* make script a cli with docopt ([af46da8](https://github.com/agrc/swapper/commit/af46da84cc2f501f9a410dd8e02b4232266327cb))
* use dotenv to configure configurable items ([904ce0e](https://github.com/agrc/swapper/commit/904ce0e6688134a7d3dd24359d46fd89b89a2be9))


### 🐛 Bug Fixes

* add sde schema back to locks query ([1661fb3](https://github.com/agrc/swapper/commit/1661fb38714bc96ac67c48c8542f38727069c1bc))
* add users param to cli ([7bad7c2](https://github.com/agrc/swapper/commit/7bad7c21fd4133eedad7bb44c88ac34444171361))
* delete temp fc if it already exists in external ([dc156bc](https://github.com/agrc/swapper/commit/dc156bc0927fe3d05496af98afd27ee09b069e23))
* don't use string mapping ([1da8ec7](https://github.com/agrc/swapper/commit/1da8ec76ce934fc4e09960725c0338a62bcfc9fe))
* exclude raster datasets ([9c26a38](https://github.com/agrc/swapper/commit/9c26a381382d55f469b8165b1751a099d793d9b6))
* fix bug causing incorrect delete error message ([bd9b18e](https://github.com/agrc/swapper/commit/bd9b18eeb50563a6a3178a5174d3184bad1df18f))
* fix incorrect title in metadata after renaming ([862f06c](https://github.com/agrc/swapper/commit/862f06c2ac728c74f048723c455bf9c076ccd1ca)), closes [#6](https://github.com/agrc/swapper/issues/6)
* fix most linting errors ([5ba23ad](https://github.com/agrc/swapper/commit/5ba23ad2a50936aa92dca4e509f426dec6efe07f))
* fix project name in coverage report param ([f935ed0](https://github.com/agrc/swapper/commit/f935ed0b4ff9e315c88598010fc6fd67cfcff63b))
* make delete_locks more generic ([b37e551](https://github.com/agrc/swapper/commit/b37e5514edc37d3e5a0cd235d11e6e7f1134bbd1))
* make Path()'s more arcpy-friendly ([e11b7fd](https://github.com/agrc/swapper/commit/e11b7fda529eb9ed439055b229d7a092ab3dc952))
* more project specific environment variable names ([214391d](https://github.com/agrc/swapper/commit/214391dfd1f9b10c64f869dcc5f78e5657ac641f))
* one more path fix for arcpy ([91a0c90](https://github.com/agrc/swapper/commit/91a0c902c28c2da7c5e79d7ed54492995c6249e1))
* only worry about datasets with traditional OBJECTID ([2f937fa](https://github.com/agrc/swapper/commit/2f937fa939018058de2c24d934eebfa634458b10))
* over trimming characters ([7203420](https://github.com/agrc/swapper/commit/7203420628f913c26125366a2269eded97caad7f))
* prevent compare from renaming swapped tables ([2251adc](https://github.com/agrc/swapper/commit/2251adcd47bc38c982d58bbc3a82a604eb9d549d))
* put the : on the right side ([b7d40b1](https://github.com/agrc/swapper/commit/b7d40b1da652c2f2580e77b8239354cc2f8ebe8b))
* raise exceptions on errors rather than just printing statements ([3adec18](https://github.com/agrc/swapper/commit/3adec18e72da276ea00d617c9754c8fd3e38e21a))
* remove extra print statement ([dc949f0](https://github.com/agrc/swapper/commit/dc949f0e9a338b15e50fdb90a1d94ced8f479e4e))
* remove extra print statements ([4c5c365](https://github.com/agrc/swapper/commit/4c5c365579540983ad48823fab2db19218e47ee2))
* remove unnecessary imports and sort them ([7337563](https://github.com/agrc/swapper/commit/7337563bd085e3c7d78922a5d3470079694a91fa))
* spelling ([e7f8c5f](https://github.com/agrc/swapper/commit/e7f8c5f9cc339ab9e5495663ff34a6209bbe2dde))


### 📖 Documentation Improvements

* add deprecation note ([f0ed167](https://github.com/agrc/swapper/commit/f0ed1679e84c142627c4299b16f0635f8e8ca431))
* add development setup instructions ([28c3381](https://github.com/agrc/swapper/commit/28c33812d07a3f07ffda05b192abe91921b15b5e))
* remove deprecation note ([ee7325c](https://github.com/agrc/swapper/commit/ee7325ce8e799683f9b211b2a3b0c988112330ef))
* setup and usage ([8fa8ca7](https://github.com/agrc/swapper/commit/8fa8ca7ee215341c1e8a5070c4306a12f56e892a))
* update env var docs ([b1b144a](https://github.com/agrc/swapper/commit/b1b144a718e9fa8ce03f858226cfadb3d82d82b8))
* update project name ([7543d2a](https://github.com/agrc/swapper/commit/7543d2aa31e133b0b0f2ea845d02bced0b3f83b0))
* use markdown ([33c4dba](https://github.com/agrc/swapper/commit/33c4dba044c0282ce02db0b16c5772a28cdcf37d))


### 🎨 Design Improvements

* sort imports ([14f08a5](https://github.com/agrc/swapper/commit/14f08a532b9bf246cf4426460c9fedb307f7f27c))
* update white space and remove comments ([63170bb](https://github.com/agrc/swapper/commit/63170bbc27db4aeb7bfd8cb3d7b4bca517cd91f7))
* use arcpy namespaces ([287d73a](https://github.com/agrc/swapper/commit/287d73a7ad2819d069c255e42e8fab7c0f6cd15d))
* yapf format ([d95abe1](https://github.com/agrc/swapper/commit/d95abe149366efaf6b8ddb2380d6cb71b881ef33))
